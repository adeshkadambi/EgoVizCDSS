# Flask API for YOLOv2 + darkflow hand detection model. 
from flask import Flask, jsonify, request, redirect, url_for
from flask_cors import CORS
import os, cv2, subprocess, sys
from werkzeug.utils import secure_filename
from PIL import Image
from pathlib import Path
import numpy as np
import pandas as pd
import ffmpeg

# == Load and import darkflow model == 
subprocess.check_call([sys.executable, "-m", "pip", "install", '-e', './detection_models/darkflow'])
from detection_models.darkflow.darkflow.net.build import TFNet

app = Flask(__name__)
CORS(app)

# == Global Variables ==
FRAMERATE = 2
ALLOWED_EXTENSIONS = {'mp4', 'avi'}

# == Miscellaneous functions ==
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_hand_presence(pred_result):
	num_frames = len(pred_result)
	num_empty = 0
	num_R = 0
	num_L = 0
	for result in pred_result:
		if not result:
			num_empty += 1
		else:
			for hand in result:
				if (hand['label'] == 'R'):
					num_R += 1
				elif (hand['label'] == 'L'):
					num_L += 1
	hand_presence = {'L':(num_L/num_frames), 'R':(num_R/num_frames), 'Empty':(num_empty/num_frames),
					'num_L':num_L, 'num_R':num_R, 'num_empty':num_empty, 'frames':num_frames}
	return(hand_presence)

# == Load YOLOv2 model == 
options = {"model": os.path.join("detection_models", "darkflow", "cfg", "yolov2_hand.cfg"), 
		   "load": os.path.join("detection_models", "darkflow", "weights", "yolov2_hand.weights"), 
		   "threshold": 0.15,
		#    "gpu": 1.0,	# Enable if running on a CUDA-available machine
		   "config": os.path.join("detection_models", "darkflow", "cfg")}
tfnet = TFNet(options)

# == Server functions ==
@app.route("/", methods=['GET'])
def home():
	return "Welcome to the app"

# Upload + predict function
@app.route("/uploadpredict/", methods=['GET', 'POST'])
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
	    .run(capture_stdout=True)
	)
	video = (
	    np
	    .frombuffer(out, np.uint8)
	    .reshape([-1, height, width, 3])
	)

	# Get YOLO prediction results for each frame
	pred_result = []
	for i in range(0, video.shape[0]):
		pred_result.append(tfnet.return_predict(video[i]))

	# Delete the temporary saved file
	os.remove(filepath)

	hand_presence = get_hand_presence(pred_result)
	return jsonify(hand_presence)


if __name__ == '__main__':
	app.run(debug=True)
