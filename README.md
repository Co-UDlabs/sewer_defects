# Sewer Defects

![License](https://img.shields.io/github/license/ehsankazemi47/sewer_defects)

This Python project repository focuses on processing CCTV images of sewer pipes and provides multiple functionalities, including defect detection using the YOLO v8 model, camera calibration, and object size estimation. The project utilizes the Ultralytics YOLO v8 model for defect detection and provides modules for camera calibration using the Checkerboard and Box methods. It also offers object size estimation by leveraging a reference object in the video.

## Structure

The repository has the following structure:

sewer_defects/
+-- cloudlabs/
¦   +-- data/
¦   +-- examples/
¦   ¦   +-- camera_calibration_examples/
¦   ¦   ¦   +-- calib_box.ipynb
¦   ¦   ¦   +-- calib_checkerboard.ipynb
¦   ¦   +-- defect_detection_examples/
¦   ¦   ¦   +-- check_data.ipynb
¦   ¦   ¦   +-- check_data.py
¦   ¦   ¦   +-- prepare_data.ipynb
¦   ¦   ¦   +-- prepare_data.py
¦   ¦   ¦   +-- train_and_test.ipynb
¦   ¦   ¦   +-- detect_unseen.ipynb
¦   ¦   +-- object_size_estimation_examples/
¦   ¦   ¦   +-- object_size.ipynb
¦   ¦   ¦   +-- object_size.py
¦   +-- src/
¦   ¦   +-- defect_detection/
¦   ¦   ¦   +-- __init__.py
¦   ¦   ¦   +-- check_data.py
¦   ¦   ¦   +-- prepare_data.py
¦   ¦   ¦   +-- model_training.py
¦   ¦   ¦   +-- prediction.py
¦   ¦   +-- camera_calibration/
¦   ¦   ¦   +-- __init__.py
¦   ¦   ¦   +-- calib_box.py
¦   ¦   ¦   +-- calib_checkerboard.py
¦   ¦   +-- object_size_estimation/
¦   ¦   ¦   +-- __init__.py
¦   ¦   ¦   +-- distance_and_size.py
¦   ¦   ¦   +-- object_size.py
¦   +-- trained_models/
+-- ultralytics/
+-- assets/
+-- models/
+-- yolo/
+-- tracker/
+-- hub/
+-- nn/


## Functionality

### 1. Defect Detection

The project utilizes the YOLO v8 model provided by Ultralytics for detecting defects in sewer pipes. To use this functionality, follow these steps:

- Collect images of defects and label them using [YoloLabel](https://github.com/developer0hye/Yolo_Label).
- Create a folder on your computer named `data` or `sewer defect data` and store the labeled images and their corresponding label files in a subfolder named `labelled_images`.
- Check the data using the `check_data.ipynb` notebook or the `check_data.py` GUI provided in the `examples` folder.
- Prepare the data for model training using the `prepare_data.ipynb` notebook or the `prepare_data.py` GUI in the `examples` folder. This process splits the data into training, validation, and test subsets and copies them into the `data` folder under `cloudlabs`. Modify the `data.yaml` file in the `data` folder accordingly. The YOLO model will read this file for training and validation.
- Train and test the model using the `train_and_test.ipynb` notebook in the `examples` folder. The trained models will be saved under `cloudlabs/trained_models`.
- To predict defects in unseen images, use the `detect_unseen.ipynb` notebook in the `examples` folder.

### 2. Camera Calibration

The project provides two methods for calibrating a camera: Checkerboard and Box. These methods are useful when the specifications, especially the focal length, of the camera recording the images are unknown.

- To calibrate the camera using a checkerboard image, use the `calib_checkerboard.ipynb` notebook in the `camera_calibration_examples` folder.
- To calibrate the camera using a labeled object with a known size, use the `calib_box.ipynb` notebook in the `camera_calibration_examples` folder.

These calibration models can be applied to videos or groups of still images. The outputs of the models include the calibration matrix from which the focal length can be obtained.

### 3. Object Size Estimation

The project provides modules for measuring the size of an object in a video. This functionality is useful for mapping the detected defects to standard defect classifications based on their sizes and positions.

To measure the size of an object, follow these steps:

- Calibrate the camera (if the focal length is unknown) using either the `calib_checkerboard.ipynb` or `calib_box.ipynb` notebook, depending on the availability of a checkerboard image.
- Use the `object_size.ipynb` notebook or the `object_size.py` GUI provided in the `object_size_estimation_examples` folder to estimate the size of an object based on the known size of a reference object, such as a joint. This functionality requires the focal length of the camera and a reference object in the video.

## Examples

The `examples` folder contains Jupyter notebooks (`.ipynb`) and Python GUI (`.py`) files demonstrating how to use the different functionalities of the project. The notebooks provide step-by-step instructions and can be modified for specific applications.

To use the provided examples:

1. Clone this repository to your local machine.
2. Install the required dependencies mentioned in the `requirements.txt` file.
3. Follow the instructions in each example file to run the desired functionality.

## Data

A sample dataset is provided in this [Google Drive folder](https://drive.google.com/drive/u/1/folders/1BoLSWbCj6WimaW4-Wca3CPkpgW5HJUqH) for testing and experimentation purposes. Please note that the labeled images included in the dataset are a small sample and may not yield accurate results when training the defect detection model. However, these images are freely available for use, and as long as you cite this project, there are no copyright issues (see [project license](https://github.com/ehsankazemi47/sewer_defects/blob/coudlabs/LICENSE)).

## License

This project is licensed under the [MIT License](LICENSE).
