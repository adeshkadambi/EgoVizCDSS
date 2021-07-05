import numpy as np
import torch
import os
import cv2
from demo import _get_image_blob
from matplotlib.pyplot import imshow

from model.faster_rcnn.resnet import resnet
from model.utils.config import cfg
from model.roi_layers import nms
from model.rpn.bbox_transform import clip_boxes, bbox_transform_inv
from model.utils.net_utils import vis_detections_filtered_objects_PIL, filter_object

try:
	xrange          # Python 2
except NameError:
	xrange = range  # Python 3

model_dir = 'models' + "/" + "res101" + "_handobj_100K" + "/" + "pascal_voc"
load_name = os.path.join(model_dir, 'faster_rcnn_1_8_132028.pth')
pascal_classes = np.asarray(['__background__', 'targetobject', 'hand']) 
fasterRCNN = resnet(pascal_classes, 101, pretrained=False)
fasterRCNN.create_architecture()
checkpoint = torch.load(load_name, map_location=(lambda storage, loc: storage))
fasterRCNN.load_state_dict(checkpoint['model'])

if 'pooling_mode' in checkpoint.keys():
	cfg.POOLING_MODE = checkpoint['pooling_mode']

# initilize the tensor holder here.
im_data = torch.FloatTensor(1)
im_info = torch.FloatTensor(1)
num_boxes = torch.LongTensor(1)
gt_boxes = torch.FloatTensor(1)
box_info = torch.FloatTensor(1) 

with torch.no_grad():
	fasterRCNN.eval()
	thresh_hand = 0.5
	thresh_obj = 0.5

	imglist = os.listdir('images/spoon_vid')
	num_images = len(imglist) - 1
	while(num_images >= 0):
		num_images -= 1
		im_file = os.path.join('images/spoon_vid', imglist[num_images])
		im_in = cv2.imread(im_file)
		im = im_in

		blobs, im_scales = _get_image_blob(im)
		assert len(im_scales) == 1, "Only single-image batch implemented"

		im_blob = blobs
		im_info_np = np.array([[im_blob.shape[1], im_blob.shape[2], im_scales[0]]], dtype=np.float32)

		im_data_pt = torch.from_numpy(im_blob)
		im_data_pt = im_data_pt.permute(0, 3, 1, 2)
		im_info_pt = torch.from_numpy(im_info_np)

		with torch.no_grad():
			im_data.resize_(im_data_pt.size()).copy_(im_data_pt)
			im_info.resize_(im_info_pt.size()).copy_(im_info_pt)
			gt_boxes.resize_(1, 1, 5).zero_()
			num_boxes.resize_(1).zero_()
			box_info.resize_(1, 1, 5).zero_() 

		rois, cls_prob, bbox_pred, \
		rpn_loss_cls, rpn_loss_box, \
		RCNN_loss_cls, RCNN_loss_bbox, \
		rois_label, loss_list = fasterRCNN(im_data, im_info, gt_boxes, num_boxes, box_info) 

		# extact predicted params
		contact_vector = loss_list[0][0] # hand contact state info
		offset_vector = loss_list[1][0].detach() # offset vector (factored into a unit vector and a magnitude)
		lr_vector = loss_list[2][0].detach() # hand side info (left/right)

		# get hand contact 
		_, contact_indices = torch.max(contact_vector, 2)
		contact_indices = contact_indices.squeeze(0).unsqueeze(-1).float()

		# get hand side 
		lr = torch.sigmoid(lr_vector) > 0.5
		lr = lr.squeeze(0).float()

		boxes = rois.data[:, :, 1:5]
		scores = cls_prob.data
		scores = scores.squeeze()

		# Apply bounding-box regression deltas
		box_deltas = bbox_pred.data
		if cfg.TRAIN.BBOX_NORMALIZE_TARGETS_PRECOMPUTED:
			# Optionally normalize targets by a precomputed mean and stdev
			box_deltas = box_deltas.view(-1, 4) * torch.FloatTensor(cfg.TRAIN.BBOX_NORMALIZE_STDS) \
		          		+ torch.FloatTensor(cfg.TRAIN.BBOX_NORMALIZE_MEANS)
			box_deltas = box_deltas.view(1, -1, 4 * len(pascal_classes))

		pred_boxes = bbox_transform_inv(boxes, box_deltas, 1)
		pred_boxes = clip_boxes(pred_boxes, im_info.data, 1)
		pred_boxes /= im_scales[0]
		pred_boxes = pred_boxes.squeeze()

		im2show = np.copy(im)
		obj_dets, hand_dets = None, None
		for j in xrange(1, len(pascal_classes)):
			if pascal_classes[j] == 'hand':
				inds = torch.nonzero(scores[:,j]>thresh_hand).view(-1)
			elif pascal_classes[j] == 'targetobject':
				inds = torch.nonzero(scores[:,j]>thresh_obj).view(-1)

			# if there is det
			if inds.numel() > 0:
				cls_scores = scores[:,j][inds]
				_, order = torch.sort(cls_scores, 0, True)
				cls_boxes = pred_boxes[inds, :]
				cls_dets = torch.cat((cls_boxes, cls_scores.unsqueeze(1), contact_indices[inds], offset_vector.squeeze(0)[inds], lr[inds]), 1)
				cls_dets = cls_dets[order]
				keep = nms(cls_boxes[order, :], cls_scores[order], cfg.TEST.NMS)
				cls_dets = cls_dets[keep.view(-1).long()]
				if pascal_classes[j] == 'targetobject':
				  obj_dets = cls_dets.cpu().numpy()
				if pascal_classes[j] == 'hand':
				  hand_dets = cls_dets.cpu().numpy()

		# im2show = vis_detections_filtered_objects_PIL(im2show, obj_dets, hand_dets, thresh_hand, thresh_obj)

		print("NUM: " + str(num_images))
		print("obj_dets: " + str(obj_dets[:,4]))
		print("hand_dets: " + str(hand_dets[:,4]))
		
		if (obj_dets is not None) and (hand_dets is not None):
			img_obj_id = filter_object(obj_dets, hand_dets)
			for obj_idx, i in enumerate(range(np.minimum(10, obj_dets.shape[0]))):
				score = obj_dets[i, 4]
				# if score > thresh_obj and i in img_obj_id:
					# print("Object detected: " + str(score))

			for hand_idx, i in enumerate(range(np.minimum(10, hand_dets.shape[0]))):
				score = hand_dets[i, 4]
				lr = hand_dets[i, -1]
				state = hand_dets[i, 5]
				# if score > thresh_hand:
					# viz hand by PIL
					# print("Hand detected: " + str(score))

					# if state > 0: # in contact hand
						# print("Contact hand: " + str(lr))