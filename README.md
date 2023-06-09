# Sewer Defects Processing Project

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/ehsankazemi47/sewer_defects/blob/coudlabs/LICENSE)

## Table of Contents
- [Introduction](#introduction)
- [Functionalities](#functionalities)
- [Project Structure](#project-structure)
- [Usage](#usage)
  - [Defect Detection](#defect-detection)
  - [Camera Calibration](#camera-calibration)
  - [Object Size Estimation](#object-size-estimation)
- [Data and Examples](#data-and-examples)
- [License](#license)

## Introduction

The Sewer Defects Processing Project is a Python-based project designed for processing CCTV images of sewer pipes. It aims to provide functionalities for detecting defects, calibrating cameras, and estimating object sizes in the captured images. This README file provides an overview of the project, its functionalities, and instructions on how to use them effectively.

## Functionalities

1. **Defect Detection**: The main functionality of the project is to use the YOLO v8 model for detecting defects in sewer pipes. It leverages the labeled images of sewer defects to train a deep learning model using YOLO v8. The trained model can then be used to detect defects in new images of sewer pipes. The YOLO v8 implementation from Ultralytics is utilized for this purpose. You can find the YOLO v8 model [here](https://github.com/ultralytics/ultralytics), and the YoloLabel tool for labeling images [here](https://github.com/developer0hye/Yolo_Label).

2. **Camera Calibration**: The project provides functionality to calibrate a camera used for recording the sewer pipe images. Camera calibration is useful when the camera specifications, particularly the focal length, are unknown. The project offers two calibration methods:
   - **Checkerboard**: This method calibrates the camera using an image of a checkerboard captured by the camera. The calibration process is implemented in the `calib_checkerboard.py` module.
   - **Box**: If a checkerboard image is not available, the "Box" method can be used to calibrate the camera. It involves labeling an object with a known size and using images of the object from different distances. The `calib_box.py` module handles the calibration process for both videos and groups of still images.

3. **Object Size Estimation**: The project includes modules for measuring the size of objects in the sewer pipe images. This functionality is particularly useful for mapping detected defects to standard defect classifications based on their sizes and positions. The object size estimation requires the focal length of the camera and a reference object in the video. Joints in CCTV images of sewer pipes are commonly used as reference objects since their size is usually known. The `object_size.py` module estimates the size of objects based on the known size of the reference object.

## Project Structure

The project repository has the following structure:

sewer_defects/
+-- cloudlabs/
¦ +-- data/
¦ +-- examples/
¦ ¦ +-- camera_calibration_examples/
¦ ¦ ¦ +-- calib_box.ipynb
¦ ¦ ¦ +-- calib_checkerboard.ipynb
¦ ¦ +-- defect_detection_examples/
¦ ¦ ¦ +-- check_data.ipynb
¦ ¦ ¦ +-- check_data.py
¦ ¦ ¦ +-- prepare_data.ipynb
¦ ¦ ¦ +-- prepare_data.py
¦ ¦ ¦ +-- train_and_test.ipynb
¦ ¦ ¦ +-- detect_unseen.ipynb
¦ ¦ +-- object_size_estimation_examples/
¦ ¦ +-- object_size.ipynb
¦ ¦ +-- object_size.py
¦ +-- src/
¦ ¦ +-- defect_detection/
¦ ¦ ¦ +-- init.py
¦ ¦ ¦ +-- check_data.py
¦ ¦ ¦ +-- prepare_data.py
¦ ¦ ¦ +-- model_training.py
¦ ¦ ¦ +-- prediction.py
¦ ¦ +-- camera_calibration/
¦ ¦ ¦ +-- init.py
¦ ¦ ¦ +-- calib_box.py
¦ ¦ ¦ +-- calib_checkerboard.py
¦ ¦ +-- object_size_estimation/
¦ ¦ +-- init.py
¦ ¦ +-- distance_and_size.py
¦ ¦ +-- object_size.py
¦ +-- trained_models/
+-- ultralytics/
+-- assets/
+-- models/
+-- yolo/
+-- tracker/
+-- hub/
+-- nn/


The YOLO model is located under the `ultralytics` directory, while the sewer defect models are located under the `cloudlabs` directory. The `src` directory contains the source code for the defect detection, camera calibration, and object size estimation modules.

## Usage

To effectively use the functionalities provided by the Sewer Defects Processing Project, follow the instructions outlined below.

### Defect Detection

1. Collect images of sewer defects and label them using the YoloLabel tool. The defects are categorized as follows: 'obstacle - Block', 'obstacle - deposit', 'obstacle - tree root', 'joint', 'crack', 'damage - hole', 'damage - severe', and 'corrosion'. The defect IDs used in the model functions are `ObsBlc`, `ObsDep`, `ObsRot`, `Jnt`, `Crk`, `DmgHol`, `DmgSev`, and `Cor`, respectively.

2. Create a folder on your computer to store the labeled images and labels (text files). Name the folder something like 'data' or 'sewer defect data', and create a subfolder named 'labelled_images' inside it.

3. Use the `check_data.ipynb` notebook or the `check_data.py` GUI under the `examples/defect_detection_examples` directory to check the data for any issues or inconsistencies. This step ensures that your labeled data is in the correct format and ready for model training.

4. Prepare the data for model training using the `prepare_data.ipynb` notebook or the `prepare_data.py` GUI under the `examples/defect_detection_examples` directory. This process will split the data into three subsets: training, validation, and testing. The subsets will be copied into the 'data' folder under `cloudlabs`. Modify the `data.yaml` file under the `data` folder accordingly. The YOLO model will read this file to use the data for training and validation.

5. Train and test the model using the `train_and_test.ipynb` notebook under the `examples/defect_detection_examples` directory. The trained model will be saved in the `trained_models` directory under `cloudlabs`.

6. Use the trained model to detect unseen defects in new images using the `detect_unseen.ipynb` notebook under the `examples/defect_detection_examples` directory. This notebook will load the trained model and detect defects in the provided test images.

### Camera Calibration

1. For camera calibration, two methods are available: Checkerboard and Box.

   - **Checkerboard**: Capture an image of a checkerboard using the same camera used for recording the sewer pipe images. Run the `calib_checkerboard.ipynb` notebook under the `examples/camera_calibration_examples` directory. This notebook will calibrate the camera using the captured checkerboard image and provide the camera matrix and distortion coefficients.

   - **Box**: If a checkerboard image is not available, you can use the Box method. This method requires images of a known-sized object (e.g., a reference joint) captured from different distances. Run the `calib_box.ipynb` notebook under the `examples/camera_calibration_examples` directory to calibrate the camera using this method. The notebook will guide you through the calibration process.

### Object Size Estimation

To estimate the size of objects in sewer pipe images:

1. Determine the focal length of the camera used for capturing the images. This information is required for accurate size estimation.

2. Identify a reference object in the sewer pipe images with a known size. Joints in CCTV images of sewer pipes are commonly used as reference objects.

3. Run the `object_size.ipynb` notebook under the `examples/object_size_estimation_examples` directory. This notebook will estimate the size of objects in the images based on the known size of the reference object and the camera focal length.

## Data and Examples

For sample data and examples on how to use the Sewer Defects Processing Project, please refer to the [`examples`](./examples) directory in the repository. It contains step-by-step notebooks and scripts for defect detection, camera calibration, and object size estimation.

## License

This project is licensed under the [MIT License](./LICENSE). Feel free to use and modify the code according to your needs.
