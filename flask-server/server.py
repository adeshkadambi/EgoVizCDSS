from flask import Flask, jsonify, request, redirect, url_for
from flask_cors import CORS
from keras.models import load_model
from keras.preprocessing import image
from werkzeug.utils import secure_filename
from PIL import Image
import os, torchvision
import numpy as np
import pandas as pd

app = Flask(__name__)
CORS(app)

# == Global Variables ==
UPLOAD_FOLDER = os.path.abspath(r'D:\Documents\Lab2\Practice\testProj2\FlaskServer\Upload') 
MODELPATH = os.path.abspath(r'Model-20-0.6544-0.7271.hdf5')
ALLOWED_EXTENSIONS = {'jpg', 'png'}
IMG_SIZE = [224, 224]

model = load_model(MODELPATH)

# == Miscellaneous functions ==
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# == Server functions ==
@app.route("/", methods=['GET'])
def index():
    return "Welcome to the app"

# template
@app.route("/weatherReport/", methods=['GET'])
def WeatherReport():
    global weather
    return 

# Upload + predict function
@app.route("/uploadpredict/", methods=['GET', 'POST'])
def UploadPredict():
    file = request.files['input_file']
    # Save input file to disk
    # if file and allowed_file(file.filename):
    #     filename = secure_filename(file.filename)
    #     file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))  # Save uploaded file to disk

    # Open and make prediction on input
    img_raw = Image.open(file)
    img_rz = img_raw.resize((IMG_SIZE[0], IMG_SIZE[1]))
    img_ar = image.img_to_array(img_rz)
    img_ar = np.expand_dims(img_ar, axis=0)
    images = np.vstack([img_ar])

    classes = model.predict(images, batch_size=10)
    return pd.Series(classes[0]).to_json(orient="values")
    # return jsonify(dict({'prediction':classes}))
    # return(jsonify("success 1"))


if __name__ == '__main__':
    app.run(debug=True)