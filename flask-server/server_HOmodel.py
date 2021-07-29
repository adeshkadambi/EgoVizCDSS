# Flask API for YOLOv2 + darkflow hand detection model. 
from flask import Flask, json, jsonify, request, redirect, url_for
from flask_cors import CORS, cross_origin
import os, cv2, subprocess, sys
from werkzeug.utils import secure_filename
from PIL import Image
from pathlib import Path
import numpy as np
import pandas as pd
import ffmpeg
import torch

from functions.global_functions import allowed_file, safe_divide
from functions.handobj_functions import get_HO_prediction

from detection_models.hand_obj.lib.model.faster_rcnn.resnet import resnet
from detection_models.hand_obj.lib.model.utils.config import cfg, cfg_from_file

app = Flask(__name__)
CORS(app, allow_headers=['Content-Type', 'Access-Control-Allow-Origin',
                         'Access-Control-Allow-Headers', 'Access-Control-Allow-Methods'])

# Allow Cross-origin requests.
@app.after_request
def apply_caching(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "GET,HEAD,POST"
    response.headers["Access-Control-Allow-Headers"] = \
        "Access-Control-Allow-Headers,  Access-Control-Allow-Origin, Origin,Accept, " + \
        "X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers"
    return response

# == Global Variables ==
FRAMERATE = 2
ALLOWED_EXTENSIONS = {'mp4', 'avi'}

# == Server functions ==
@app.route("/", methods=['GET'])
def home():
	return "Welcome to the app"

@cross_origin(origin='*',headers=['Content-Type','Authorization'])

# Upload + predict function
@app.route("/uploadpredictHO/", methods=['GET', 'POST'])
def UploadPredict():
	file = request.files['input_file']
	# Save input file to disk (temporary)
	if file and allowed_file(file.filename, ALLOWED_EXTENSIONS):
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
		# .run(capture_stdout=True)
	)
	video = (
		np
		.frombuffer(out, np.uint8)
		.reshape([-1, height, width, 3])
	)

	# Delete the temporary saved file
	os.remove(filepath)

	# Get prediction from Hand-Obj (Shan) model
	l_int, r_int, l_dur, r_dur, l_num, r_num = get_HO_prediction(fasterRCNN, video, pascal_classes, thresh_hand, thresh_obj)

	response = jsonify({"l_int":l_int, "r_int":r_int, "l_dur":l_dur, "r_dur":r_dur, "l_num":l_num, "r_num":r_num})
	# Allow Cross-origin request (request from same IP)
	response.headers.add('Access-Control-Allow-Origin', '*')
	return response


if __name__ == '__main__':
	# == Load resnet101 model == 
	# Initialize variables
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

	# Run the Flask app
	app.run(debug=True, port=5000, host="0.0.0.0")
	# app.run(debug=True, port=5000)
