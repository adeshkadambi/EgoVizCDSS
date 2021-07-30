# Flask Code Documentation

## Introduction
A detailed explanation of the Flask server code, with `server_HOmodel.py` as the main example. 

## Detailed Code Runthrough
### Imports
The necessary imports for the python code.

### Flask starter code 
```
app = Flask(__name__)
CORS(app, allow_headers=['Content-Type', 'Access-Control-Allow-Origin',
```
These lines are necessary to begin a Flask project. Note that typically `CORS(app)` is all that is required for the second line, but the additional options were added for Docker compatibility. 

```
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
```
The above code is added for Docker compatibility (allow for Cross-Origin requests from Docker). It has not be thoroughly tested, but it may actually be unnecessary.

### Global Variables
May want to use more global variables for easier adjustment in the future.

### Server functions
A Flask API routes Python functions to specific URLs. To access these functions, typically an HTML request (usually POST or GET) is sent to the URL. 

```
@app.route("/", methods=['GET'])
def home():
	return "Welcome to the app"
```
Above is just a simple test routing for debugging purposes.

```
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
```
Here is another line added for Docker compatibility with CORS. There may be some security risks involved with `origin='*'` ; this may need to be looked into. 

```
@app.route("/uploadpredictHO/", methods=['GET', 'POST'])
def UploadPredict():
	file = request.files['input_file']
	# Save input file to disk (temporary)
	if file and allowed_file(file.filename, ALLOWED_EXTENSIONS):
		Path("./upload_temp/").mkdir(exist_ok=True)
		filename = secure_filename(file.filename)
		filepath = os.path.join("upload_temp", filename)
		file.save(filepath)  # Save uploaded file to disk
```
Above is the start of the main function of the Hand-Object API. First, the video file is obtained via POST method and temporarily saved to disk. The `allowed_file` method is used, which is imported from `global_functions.py`. The file is temporarily saved to disk because the file is generally too large to manipulate with only Python variables. Also, ffmpeg works best with saved files rather than Python variables.

```
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
```
Here, ffmpeg is used to convert the saved video into a numpy array of frames at the target FRAMERATE (default is 2 fps). 

```
	# Delete the temporary saved file
	os.remove(filepath)

	# Get prediction from Hand-Obj (Shan) model
	l_int, r_int, l_dur, r_dur, l_num, r_num = get_HO_prediction(fasterRCNN, video, pascal_classes, thresh_hand, thresh_obj)

	response = jsonify({"l_int":l_int, "r_int":r_int, "l_dur":l_dur, "r_dur":r_dur, "l_num":l_num, "r_num":r_num})
	# Allow Cross-origin request (request from same IP)
	response.headers.add('Access-Control-Allow-Origin', '*')
	return response
```
The temporary file is deleted and the video frames are passed to the prediction function `get_HO_prediction()`, which is defined in `handobj_functions.py`. This function uses the Hand-Object model to detect hand-object interactions and returns the following metrics:

* Percentage of hand interaction for the entire video
* Average interaction duration
* Average number of interactions per hour

These metrics are divided for each hand, as well as each type of interaction state:

* No contact (N)
* Self-contact (S)
* Another person (O)
* Portable object (P)
* Stationary object (F)
* Total interactions (T)

The metrics are returned as a dictionary, with the interaction state as the keys. The dictionary is then converted into JSON format and a CORS header is added for Docker compatibilty with CORS. The final output of the API is a JSON-formatted dictionary with each of the metrics as outputs.

### Main Method
```
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
```
The majority of the main method begins with loading the Hand-Object model. Key variables defined here are `thresh_hand` and `thresh_obj`, which are the thresholds for hand/object detection for the model. By default, they are set to 0.5. The code for loading the model is taken almost directly from `demo.py`, the demo code provided by the authors of the Hand-Object model. This can be found in `detection_models/hand_obj/demo.py`.

```
	# Run the Flask app
	app.run(debug=True, port=5000, host="0.0.0.0")
```

This is the call to run the Flask application. A decription of the arguments:
* `debug=True` enables debug mode, which reloads the application whenever the code to `server_HOmodel.py` is changed (very useful for development).
* `port=5000` specifies which port to run the application on. By default, port 5000 is used if unspecified. 
* `host="0.0.0.0"` defines the hostname to listen on. Host 0.0.0.0 must be used for external applications (such as Docker).