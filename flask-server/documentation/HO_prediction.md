# Hand-Object Prediction Function Documentation

## Introduction
An explanation of `get_HO_prediction()`, the main function to extract Hand-Object interaction metrics from an egocentric video. The function is found in `functions/handobj_functions.py`.

To begin, most of the code found in this function was taken/adapted from the demo code provided in `demo.py`, found in `detection_models/hand_obj/demo.py`.

## Arguments
* **fasterRCNN** (torch model): torch model to use for predictions
* **video** (ndarray): video frames in a numpy array
* **pascal_classes** (ndarray): interaction classes in a numpy array
* **thresh_hand** (float): threshold for hand detection (must range from 0-1)
* **thresh_obj** (float): threshold for object detection (must range from 0-1)

## Returns
* **l_int** (dict): a dict containing percentage of video with left hand interaction, for each interaction state
* **r_int** (dict): a dict containing percentage of video with right hand interaction, for each interaction state
* **l_dur** (dict): a dict containing average left hand interaction duration, for each interaction state
* **r_dur** (dict): a dict containing average right hand interaction duration, for each interaction state
* **l_num** (dict): a dict containing total number of left hand interactions, for each interaction state
* **r_num** (dict): a dict containing total number of right hand interactions, for each interaction state