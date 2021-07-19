# Flask API for YOLOv2 + darkflow hand detection model. 
from flask import Flask, json, jsonify, request, redirect, url_for
from flask_cors import CORS
import os, cv2, subprocess, sys
from werkzeug.utils import secure_filename
from PIL import Image
from pathlib import Path
import numpy as np
import pandas as pd
import ffmpeg
import torch

from detection_models.hand_obj.lib.model.faster_rcnn.resnet import resnet
from detection_models.hand_obj.lib.model.rpn.bbox_transform import bbox_transform_inv
from detection_models.hand_obj.lib.model.rpn.bbox_transform import clip_boxes
from detection_models.hand_obj.lib.model.roi_layers import nms
from detection_models.hand_obj.lib.model.utils.config import cfg, cfg_from_file
from detection_models.hand_obj.lib.model.utils.blob import im_list_to_blob

app = Flask(__name__)
CORS(app)

# == Global Variables ==
FRAMERATE = 2
ALLOWED_EXTENSIONS = {'mp4', 'avi'}

# == Function Definitions == 
def allowed_file(filename):
	return '.' in filename and \
		   filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def safe_divide(n, d):
	# Safe division - return 0 if dividing by 0
	return n/d if d else 0

def _get_image_blob(im):
	"""Converts an image into a network input.
	Arguments:
	  im (ndarray): a color image in BGR order
	Returns:
	  blob (ndarray): a data blob holding an image pyramid
	  im_scale_factors (list): list of image scales (relative to im) used
		in the image pyramid
	"""
	im_orig = im.astype(np.float32, copy=True)
	im_orig -= cfg.PIXEL_MEANS

	im_shape = im_orig.shape
	im_size_min = np.min(im_shape[0:2])
	im_size_max = np.max(im_shape[0:2])

	processed_ims = []
	im_scale_factors = []

	for target_size in cfg.TEST.SCALES:
		im_scale = float(target_size) / float(im_size_min)
		# Prevent the biggest axis from being more than MAX_SIZE
		if np.round(im_scale * im_size_max) > cfg.TEST.MAX_SIZE:
			im_scale = float(cfg.TEST.MAX_SIZE) / float(im_size_max)
		im = cv2.resize(im_orig, None, None, fx=im_scale, fy=im_scale,
				interpolation=cv2.INTER_LINEAR)
		im_scale_factors.append(im_scale)
		processed_ims.append(im)

	# Create a blob to hold the input images
	blob = im_list_to_blob(processed_ims)

	return blob, np.array(im_scale_factors)

def get_interaction_percentage(hand_list, thresh_hand):
	"""Calculate percentage of video where hand interaction is detected.
	Arguments:
	  hand_list (list): a list of hand_dets data for each frame of the video
	  thresh_hand (float): threshold for hand detection confidence
	Returns:
	  l_int (dict): a list containing percentage of video with left hand interaction, for each interaction state
	  r_int (dict): a list containing percentage of video with right hand interaction, for each interaction state
	"""
	l_int = {'N':0, 'S':0, 'O':0, 'P':0, 'F':0, 'T':0}
	r_int = {'N':0, 'S':0, 'O':0, 'P':0, 'F':0, 'T':0}
	state_key = {0:'N', 1:'S', 2:'O', 3:'P', 4:'F'}
	num_frames = len(hand_list)

	# Iterate through all frames and increment for each detected interaction state
	for frame in hand_list:
		if(frame is not None):
			for hand in frame:
				score = hand[4]
				if score > thresh_hand:
					if hand[-1] == 0:   # Left hand
						l_int[state_key[hand[5]]] += 1
					else:               # Right hand
						r_int[state_key[hand[5]]] += 1
	
	# Divide all incremented frames by total number of frames to get percentage
	for key in l_int.keys():
		if key is not 'T':
			l_int[key] = np.round((l_int[key]/num_frames)*100, 1)
			r_int[key] = np.round((r_int[key]/num_frames)*100, 1)
			# Sum up total interaction
			if key is not 'N':
				l_int['T'] += l_int[key]
				r_int['T'] += r_int[key]

	return l_int, r_int

def get_avg_interaction_duration(hand_list, thresh_hand, fps=2, get_ints=False):
	"""Calculate average duration of hand interaction, for each interaction state.
	Arguments:
	  hand_list (list): a list of hand_dets data for each frame of the video
	  thresh_hand (float): threshold for hand detection confidence
	Returns:
	  l_dur (dict): a list containing average left hand interaction duration, for each interaction state
	  r_dur (dict): a list containing average right hand interaction duration, for each interaction state
	  [get_ints==True] l_num (dict): a list containing total number of left hand interactions, for each interaction state
	  [get_ints==True] r_num (dict): a list containing total number of right hand interactions, for each interaction state
	"""
	l_dur = {'N':0, 'S':0, 'O':0, 'P':0, 'F':0, 'T':0}
	r_dur = {'N':0, 'S':0, 'O':0, 'P':0, 'F':0, 'T':0}
	l_num = {'N':0, 'S':0, 'O':0, 'P':0, 'F':0, 'T':0}     	# Number of interactions
	r_num = {'N':0, 'S':0, 'O':0, 'P':0, 'F':0, 'T':0}
	state_key = {0:'N', 1:'S', 2:'O', 3:'P', 4:'F'}
	cur_state_L, cur_state_R = None, None
	dur_hrs = (len(hand_list)/FRAMERATE)/3600				# Duration of video in hours

	# Iterate through frames and calculate total interaction duration and number of interactions
	for frame in hand_list:
		if frame is not None:              
			for hand in frame:
				score = hand[4]
				state = state_key[hand[5]]
				if score > thresh_hand and hand[-1] == 0:   # Left hand
					l_dur[state] += 1
					if state != 'N': l_dur['T'] += 1
					if state != cur_state_L:                # Increment number of interactions if a different state is detected
						cur_state_L = state
						l_num[state] += 1
						if state != 'N': l_num['T'] += 1
				elif score > thresh_hand and hand[-1] == 1: # Right hand
					r_dur[state] += 1
					if state != 'N': r_dur['T'] += 1
					if state != cur_state_R:                # Increment number of interactions if a different state is detected
						cur_state_R = state
						r_num[state] += 1
						if state != 'N': r_num['T'] += 1
		else:
			cur_state_L, cur_state_R = None, None

	# Divide total interaction duration by number of interactions to get avg interaction duration
	for key in l_num.keys():      
		# Also divide by fps to get duration in seconds
		l_dur[key] = safe_divide(l_dur[key], l_num[key])/fps
		r_dur[key] = safe_divide(r_dur[key], r_num[key])/fps

		# Divide number of interactions with duration in hours to get number of interactions/hour
		l_num[key] = np.round(l_num[key]/dur_hrs, 0)
		r_num[key] = np.round(r_num[key]/dur_hrs, 0)
	
	if(get_ints):
		return l_dur, r_dur, l_num, r_num
	else:
		return l_dur, r_dur

# == Load resnet101 model == 
pascal_classes = np.asarray(['__background__', 'targetobject', 'hand']) 
thresh_hand = 0.5
thresh_obj = 0.5
cfg_file = os.path.join("detection_models", "hand_obj", "cfgs", "res101.yml")

# CFG settings
cfg_from_file(cfg_file)
cfg.USE_GPU_NMS = False
np.random.seed(cfg.RNG_SEED)

# Load model
checksession = 1
checkepoch = 8
checkpoint = 132028
model_name = 'faster_rcnn_{}_{}_{}.pth'.format(checksession, checkepoch, checkpoint)
load_name = os.path.join('detection_models', 'hand_obj', 'models', 'res101_handobj_100K', 'pascal_voc', model_name)
if (torch.cuda.is_available()):
	model = torch.load(load_name)
else:
	model = torch.load(load_name, map_location=(lambda storage, loc: storage))

# Initialize network
fasterRCNN = resnet(pascal_classes, 101, pretrained=False, class_agnostic=False)
fasterRCNN.create_architecture()
fasterRCNN.load_state_dict(model['model'])
if 'pooling_mode' in model.keys():
	cfg.POOLING_MODE = model['pooling_mode']


# == Server functions ==
@app.route("/", methods=['GET'])
def home():
	return "Welcome to the app"

# Upload + predict function
@app.route("/uploadpredictHO/", methods=['GET', 'POST'])
def UploadPredict():
	file = request.files['input_file']
	# Save input file to disk (temporary)
	if file and allowed_file(file.filename):
		Path("./upload_temp/").mkdir(exist_ok=True)
		filename = secure_filename(file.filename)
		filepath = os.path.join("upload_temp", filename)
		file.save(filepath)  # Save uploaded file to disk

	# Convert video to np array at target framerate
	probe = ffmpeg.probe(filepath)
	video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
	width = int(video_stream['width'])
	height = int(video_stream['height'])

	out, _ = (
		ffmpeg
		.input(filepath)
		.filter('fps', fps=FRAMERATE)
		.output('pipe:', format='rawvideo', pix_fmt='rgb24')
		.run(quiet=True, capture_stdout=True)
	)
	video = (
		np
		.frombuffer(out, np.uint8)
		.reshape([-1, height, width, 3])
	)

	# Initialize Flow Tensor
	im_data = torch.FloatTensor(1)
	im_info = torch.FloatTensor(1)
	num_boxes = torch.LongTensor(1)
	gt_boxes = torch.FloatTensor(1)
	box_info = torch.FloatTensor(1) 
	if (torch.cuda.is_available()):         # Ship to cuda if avaialable
		im_data = im_data.cuda()
		im_info = im_info.cuda()
		num_boxes = num_boxes.cuda()
		gt_boxes = gt_boxes.cuda()

	# Get resnet101 prediction results for each frame
	with torch.no_grad():
		if (torch.cuda.is_available()):
			fasterRCNN.cuda()
		fasterRCNN.eval()

		obj_list = []
		hand_list = []
		frame_num = 0
		for frame in video:
			blobs, im_scales = _get_image_blob(frame)
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

			scores = cls_prob.data
			boxes = rois.data[:, :, 1:5]

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

			# Apply bounding-box regression deltas
			box_deltas = bbox_pred.data
			box_deltas = box_deltas.view(-1,4) * torch.FloatTensor(cfg.TRAIN.BBOX_NORMALIZE_STDS) \
						+ torch.FloatTensor(cfg.TRAIN.BBOX_NORMALIZE_MEANS)
			box_deltas = box_deltas.view(1, -1,  4 * len(pascal_classes))

			pred_boxes = bbox_transform_inv(boxes, box_deltas, 1)
			pred_boxes = clip_boxes(pred_boxes, im_info.data, 1)

			pred_boxes /= im_scales[0]
			scores = scores.squeeze()
			pred_boxes = pred_boxes.squeeze()
			obj_dets, hand_dets = None, None
			obj_list.append(obj_dets)
			hand_list.append(hand_dets)
			for j in range(1, len(pascal_classes)):
				if pascal_classes[j] == 'hand':
					inds = torch.nonzero(scores[:,j]>thresh_hand).view(-1)
				elif pascal_classes[j] == 'targetobject':
					inds = torch.nonzero(scores[:,j]>thresh_obj).view(-1)

				# if there is det
				if inds.numel() > 0:
					cls_scores = scores[:,j][inds]
					_, order = torch.sort(cls_scores, 0, True)
					cls_boxes = pred_boxes[inds][:, j * 4:(j + 1) * 4]
			  
					cls_dets = torch.cat((cls_boxes, cls_scores.unsqueeze(1), contact_indices[inds], offset_vector.squeeze(0)[inds], lr[inds]), 1)
					cls_dets = cls_dets[order]
					keep = nms(cls_boxes[order, :], cls_scores[order], cfg.TEST.NMS)
					cls_dets = cls_dets[keep.view(-1).long()]
					if pascal_classes[j] == 'targetobject':
						obj_dets = cls_dets.cpu().numpy()
						obj_list[frame_num] = obj_dets
					if pascal_classes[j] == 'hand':
						hand_dets = cls_dets.cpu().numpy()
						hand_list[frame_num] = hand_dets
			frame_num += 1

		l_int, r_int = get_interaction_percentage(hand_list, thresh_hand)
		l_dur, r_dur, l_num, r_num = get_avg_interaction_duration(hand_list, thresh_hand, get_ints=True)

	# Delete the temporary saved file
	os.remove(filepath)

	# return [jsonify(l_int), jsonify(r_int), jsonify(l_dur), jsonify(r_dur), jsonify(l_num), jsonify(r_num)]
	# return str([l_int, r_int, l_dur, r_dur, l_num, r_num])
	return jsonify({"l_int":l_int, "r_int":r_int, "l_dur":l_dur, "r_dur":r_dur, "l_num":l_num, "r_num":r_num})


if __name__ == '__main__':
	app.run(debug=True)
