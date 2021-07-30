# EgoViz Flask Server Documentation

## Introduction

The purpose of the Flask server is to implement EgoViz machine learning models into a backend API, which can be accessed by the frontend Angular webapp.

<br>  
<br>  

## Getting started

This project uses a conda virtual environment to manage dependencies. On Linux-based systems, the environment can be created with the environment_linux.yml file: 
```
conda env create -f environment_linux.yml
conda activate handobj
```
For non-Linux-based systems, the requirements.txt file may be used to download the required dependencies **(untested)**
```
pip install -r requirements.txt
```
Furthermore, a Docker image may be built to deploy the API on any system:
```
docker build -t handobj-api . 2> log.log
docker run -p 5000:5000 handobj-api
```
*Note that the output of the docker build command is piped into a log file, for debugging purposes.*

<br>
<br>

## Building the model(s)

The architecture of this project is intended to be modular, such that each model is deployed on an independent Flask server/API.
Since each model is an individual project, they likely have their own dependencies, and will need to be built independently.
Currently, the Hand-Object model (by Shan et al.) is the only significant model that is used in this project.
To build the Hand-Object model:
```
cd detection_models/hand_obj/lib
python setup.py build develop 
```

Now that the model is built, we can go back to the main directory and run the Flask server:
```
python server_HOmodel.py
```
The Flask server should run, which can now respond to API calls from the Angular frontend. 