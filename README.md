[![Co-UDlabs](https://img.shields.io/badge/Project:-CoUDlabs-brightgreen.svg)](https://co-udlabs.eu/)
[![License](https://img.shields.io/badge/License:-Academic-blue.svg)](https://github.com/ehsankazemi47/sewer_defects/blob/coudlabs/LICENSE)
[![Citation](https://img.shields.io/badge/Acknowledgement:-Cite-yellow)](https://github.com/ehsankazemi47/sewer_defects/blob/coudlabs/CITATION.cff)

# Sewer Defects

This Python project repository focuses on processing CCTV images of sewer pipes and provides multiple functionalities, including automated defect detection, camera calibration, and defect size estimation. The project utilizes the Ultralytics YOLO v8 model for defect detection and provides modules for camera calibration using the 'Checkerboard' and 'Box' methods. It also offers object size estimation by leveraging a reference object in the video.


## Structure

The repository has the following structure:

```
sewer_defects/
├── cloudlabs/
│ ├── data/
│ ├── examples/
│ │ ├── camera_calibration_examples/
│ │ │ ├── calib_box.ipynb
│ │ │ └── calib_checkerboard.ipynb
│ │ ├── defect_detection_examples/
│ │ │ ├── check_data.ipynb
│ │ │ ├── check_data.py
│ │ │ ├── prepare_data.ipynb
│ │ │ ├── prepare_data.py
│ │ │ ├── train_and_test.ipynb
│ │ │ └── detect_unseen.ipynb
│ │ ├── object_size_estimation_examples/
│ │ │ ├── object_size.ipynb
│ │ │ └── object_size.py
| ├── src/
│ | ├── defect_detection/
│ │ | ├── init.py
│ │ | ├── check_data.py
│ │ | ├── prepare_data.py
│ │ | ├── model_training.py
│ │ | └── prediction.py
│ | ├── camera_calibration/
│ | │ ├── init.py
│ | │ ├── calib_box.py
│ | │ └── calib_checkerboard.py
│ | ├── object_size_estimation/
│ | ├── init.py
│ | ├── distance_and_size.py
│ | └── object_size.py
| └── trained_models/
├── ultralytics/
| ├── assets/
| ├── models/
| ├── yolo/
| ├── tracker/
| ├── hub/
| └── nn/
├── init.py
├── requirements.txt
├── setup.py
└── LICENSE
```


## Functionality

### 1. Defect Detection

The project utilizes the YOLO v8 model provided by Ultralytics for detecting defects in sewer pipes (for YOLO see [here](https://github.com/ultralytics/ultralytics)). The model follows these steps:

1.1. **Data collection & labelling**. Collect images of defects in sewer pipes and label them using [YoloLabel](https://github.com/developer0hye/Yolo_Label). [This video](https://drive.google.com/file/d/1CTeDLK8DkOE8SMFm0joFSnadAJ92aY35/view?usp=drive_link) shows how YoloLabel can be used to label defects in CCTV images.
Create a folder on your computer named something like `data` or `sewer defects data` and store the labeled images and their corresponding label files in a subfolder named `labelled_images`.

1.2. **Check labels**. Check the data using the [`check_data.ipynb`](https://github.com/ehsankazemi47/sewer_defects/blob/coudlabs/coudlabs/examples/defect_detection_examples/check_data.ipynb) notebook or the [`check_data.py`](https://github.com/ehsankazemi47/sewer_defects/blob/coudlabs/coudlabs/examples/defect_detection_examples/check_data.py) GUI provided in the `coudlabs/examples/defect_detection_examples` folder. An exe version of the GUI is available [here](https://drive.google.com/file/d/1L_W1-QtmBmi7BljkhNeRFYMS9lJUhPvv/view?usp=drive_link).

1.3. **Data preperation**. Prepare the data for model training using the [`prepare_data.ipynb`](https://github.com/ehsankazemi47/sewer_defects/blob/coudlabs/coudlabs/examples/defect_detection_examples/prepare_data.ipynb) notebook or the [`prepare_data.py`](https://github.com/ehsankazemi47/sewer_defects/blob/coudlabs/coudlabs/examples/defect_detection_examples/prepare_data.py) GUI in the `coudlabs/examples/defect_detection_examples` folder. An exe version of the GUI is provided at this [link](https://drive.google.com/file/d/1UYIqswJ--HOyypuYpIfMdGgno7c0WlsV/view?usp=drive_link). This process splits the data into training, validation, and test subsets and copies them into the [`data`](https://github.com/ehsankazemi47/sewer_defects/tree/coudlabs/coudlabs/data) folder under `cloudlabs`. Modify the [`data.yaml`](https://github.com/ehsankazemi47/sewer_defects/blob/coudlabs/coudlabs/data/data.yaml) file in the `cudlabs/data` folder accordingly. The YOLO model will read this file for training and validation. In this file, you need to set the path to the training dataset and list the label names in the same order used in Section 1.1 to label the defect in the images. These labels in the pcurrent version of the model are `ObsPlc`, `ObsDep`, `ObsRot`, `Jnt`, `Crk`, `DmgHol`, `DmgSev` and `Cor` denoting Obstacle - block, Obstacle - deposited, Obstacle - tree root, Joint, Crack, Damage - hole, Damage - severe (deformed, collapsed) and Corrosion, respectively.

1.4. **Train & test**. Train and test the model using the [`train_and_test.ipynb`](https://github.com/ehsankazemi47/sewer_defects/blob/coudlabs/coudlabs/examples/defect_detection_examples/train_and_test.ipynb) notebook in the `coudlabs/examples/defect_detection_examples` folder. The results of training and the trained model weights will be saved under `cloudlabs/trained_models`.

1.5. **Predcit**. To predict defects in unseen images, use the [`detect_unseen.ipynb`](https://github.com/ehsankazemi47/sewer_defects/blob/coudlabs/coudlabs/examples/defect_detection_examples/detect_unseen.ipynb) notebook in the `coudlabs/examples/defect_detection_examples` folder.

### 2. Camera Calibration

The project provides two methods for calibrating a camera: Checkerboard and Box. These methods are useful when the specifications - especially the focal length - of the camera recording the images are unknown.

2.1. **Checkerboard method**. To calibrate the camera using a checkerboard image, use the [`calib_checkerboard.ipynb`](https://github.com/ehsankazemi47/sewer_defects/blob/coudlabs/coudlabs/examples/camera_calibration_examples/calib_checkerboard.ipynb) notebook in the `coudlabs/examples/camera_calibration_examples` folder. This code can handle both video and group of images to calibrate the camera. The checkerboard shoud be moving in different directions and/or distances to the camera.

2.2. **Box method**. To calibrate the camera using an object with a known size (like a joint), label the object in images with the oject at different distances from the camera and then use the [`calib_box.ipynb`](https://github.com/ehsankazemi47/sewer_defects/blob/coudlabs/coudlabs/examples/camera_calibration_examples/calib_box.ipynb) notebook in the `coudlabs/examples/camera_calibration_examples` folder.

These calibration models can be applied to videos or groups of still images. The outputs of the models include the calibration matrix from which the focal length can be obtained.

### 3. Object Size Estimation

The project provides modules for measuring the size of an object in a video. This functionality is useful for mapping the detected defects to standard defect classifications based on their sizes and positions.

To measure the size of an object, follow these steps:

3.1. **Camera specifications**. Calibrate the camera (if the focal length is unknown) using one of the methods presented in the previous  section, depending on the availability of a checkerboard image.

3.2. **Size estimation using a reference object**. Use the [`object_size.ipynb`](https://github.com/ehsankazemi47/sewer_defects/blob/coudlabs/coudlabs/examples/object_size_estimation_examples/object_size.ipynb) notebook or the [`object_size.py`](https://github.com/ehsankazemi47/sewer_defects/blob/coudlabs/coudlabs/examples/object_size_estimation_examples/object_size.py) GUI provided in the `coudlabs/examples/object_size_estimation_examples` folder to estimate the size of an object based on the known size of a reference object, such as a joint. This functionality requires the focal length of the camera and a reference object in the video. For running this module, an exe version of the GUI is also available at this [link](https://drive.google.com/file/d/1eyXLkkjrj9-Flr6CQTzy-hC2Ya4rijXf/view?usp=drive_link).


## Usage

### 1. Defect Detection

To use the defect detection functionality, follow these steps (you can use the set of labelled images provided at this [link](https://drive.google.com/drive/u/1/folders/1N3M5Ud39WPRZuprVbn3ed1W-14b-XKLi) to follow the steps. Note that this is a small dataset provided for demonstration of the model usage - it should not be expected to achieve an accurate training / prediction using this dataset):

1. Clone the repository to your local machine.
2. Install the required dependencies mentioned in the [`requirements.txt`](https://github.com/ehsankazemi47/sewer_defects/blob/coudlabs/requirements.txt) file.
3. Navigate to the `sewer_defects/examples/defect_detection_examples` folder.
4. Open the [`check_data.ipynb`](https://github.com/ehsankazemi47/sewer_defects/blob/coudlabs/coudlabs/examples/defect_detection_examples/check_data.ipynb) notebook or run one of the GUIs ([`check_data.py`](https://github.com/ehsankazemi47/sewer_defects/blob/coudlabs/coudlabs/examples/defect_detection_examples/check_data.py) or [`check_data.exe`](https://drive.google.com/file/d/1L_W1-QtmBmi7BljkhNeRFYMS9lJUhPvv/view?usp=drive_link).
   - This will display the labeled images along with their bounding boxes to verify the correctness of the data.
   - **Input**: Path to data.
   - **Output**: Visualization of labeled images with bounding boxes.

5. Once you have verified the data, open the [`prepare_data.ipynb`](https://github.com/ehsankazemi47/sewer_defects/blob/coudlabs/coudlabs/examples/defect_detection_examples/prepare_data.ipynb) notebook or run one of the GUIs ([`prepare_data.py`](https://github.com/ehsankazemi47/sewer_defects/blob/coudlabs/coudlabs/examples/defect_detection_examples/prepare_data.py) or [`prepare_data.exe`](https://drive.google.com/file/d/1UYIqswJ--HOyypuYpIfMdGgno7c0WlsV/view?usp=drive_link)).
   - This will split the data into training, validation, and test subsets based on user preference and copy them into the `data` folder under `cloudlabs`.
   - Modify the `data.yaml` file in the `data` folder according to your dataset.
   - **Input**: Path to data and ratio for data splitting.
   - **Output**: Data split into training, validation, and test subsets in the `data` folder.

6. To train and test the defect detection model, open the [`train_and_test.ipynb`](https://github.com/ehsankazemi47/sewer_defects/blob/coudlabs/coudlabs/examples/defect_detection_examples/train_and_test.ipynb) notebook.
   - Follow the instructions provided in the notebook to train the model using the prepared data and evaluate its performance on the test set.
   - **Input**:
     - Pre-trained model name, e.g. `yolov8l.pt`.
     - Arguments to the YOLO train function, e.g. `epoches` and `imgsz`
     - Path to the data YAML containing the info about the prepared dataset (e.g., `coudlabs/data/data.yaml`).
   - **Output**: Statistics of input data, results of training, and trained model weights saved under `cloudlabs/trained_models` folder.

7. To predict defects in unseen images, open the [`detect_unseen.ipynb`](https://github.com/ehsankazemi47/sewer_defects/blob/coudlabs/coudlabs/examples/defect_detection_examples/detect_unseen.ipynb) notebook.
   - Set the paths to the trained model and the unseen images, then run the notebook.
   - **Input**:
     - `model_path`: Path to the trained model file (e.g., `cloudlabs/trained_models/model_2023-06-09-11-36-49/weights/best.pt`).
     - `image_folder`: Path to the folder containing the unseen images (e.g., `path/to/unseen/images`).
   - **Output**: Visualization of predicted defects in unseen images with confidence scores.

### 2. Camera Calibration

To calibrate the camera using the provided methods, follow these steps:

1. Collect images or videos for camera calibration. 
2. Navigate to the `sewer_defects/examples/camera_calibration_examples` folder.
3. To calibrate the camera using a checkerboard image, open the [`calib_checkerboard.ipynb`](https://github.com/ehsankazemi47/sewer_defects/blob/coudlabs/coudlabs/examples/camera_calibration_examples/calib_checkerboard.ipynb) notebook.
   - Follow the step-by-step instructions provided in the notebook to calibrate the camera and obtain the calibration matrix.
   - **Input**: Path to image; checkerboard dimensions, real size of square on the checkerboard.
   - **Output**: Calibration matrix including focal length.
   - You can use the data provided at this [link](https://drive.google.com/drive/folders/1Jd_tokxHcx2B3DwX9wiGJ3UBnIxShind?usp=drive_link) to examine the model usage.

4. To calibrate the camera using a labeled object with a known size (like a joint), open the [`calib_box.ipynb`](https://github.com/ehsankazemi47/sewer_defects/blob/coudlabs/coudlabs/examples/camera_calibration_examples/calib_box.ipynb) notebook.
   - Follow the instructions in the notebook to calibrate the camera and obtain the calibration matrix.
   - **Input**: Path to image; width and height of object.
   - **Output**: Calibration matrix including focal length.
   - You can use the data provided at this [link](https://drive.google.com/drive/u/1/folders/1QI4C71A9831hVXz8YHqBPtTgtgactjVV) to examine the model usage.

### 3. Object Size Estimation

To estimate the size of an object, follow these steps:

1. Ensure that the camera has been calibrated using either the checkerboard or box method. If the focal length is unknown, follow the camera calibration steps mentioned above.
2. The model can only estimate the size of an object in a video (sequence of frames) where a reference object (e.g., a joint) is also present. This is because a 3D problem is solved in 2D.
3. Navigate to the `sewer_defects/examples/object_size_estimation_examples` folder.
4. Open the [`object_size.ipynb`](https://github.com/ehsankazemi47/sewer_defects/blob/coudlabs/coudlabs/examples/object_size_estimation_examples/object_size.ipynb) notebook or run one of the GUIs ([`object_size.py`](https://github.com/ehsankazemi47/sewer_defects/blob/coudlabs/coudlabs/examples/object_size_estimation_examples/object_size.py) or [`object_size.exe`](https://drive.google.com/file/d/1eyXLkkjrj9-Flr6CQTzy-hC2Ya4rijXf/view?usp=drive_link)).
   - Modify the paths to the calibrated camera parameters and the video containing the reference object.
   - **Input**:
     - Path to data.
     - Camera's focal length.
     - Real size of the reference object (e.g. diameter of a pipe as the height of a joint).
   - **Output**: Estimated size of the object.
   - You can use the data provided at this [link](https://drive.google.com/drive/u/1/folders/1U2gcpszOSbs0goN-ymdrUqw5MvOlxQTJ) to test the model usage.

Please note that for each functionality, there are additional files and configurations that may need to be adjusted based on your specific dataset and requirements.


## Data

A few sample data are provided in this [Google Drive folder](https://drive.google.com/drive/u/1/folders/1BoLSWbCj6WimaW4-Wca3CPkpgW5HJUqH) for testing and experimentation purposes. Please note that the labeled images included in the dataset are a small sample and may not yield accurate results when training the defect detection model. However, these data are freely available for use, and as long as you cite this project, there are no copyright issues (see [project license](https://github.com/ehsankazemi47/sewer_defects/blob/coudlabs/LICENSE)).


## License

This project is licensed under the [Co-UDlabs Project](https://co-udlabs.eu/). Users are permitted to use, modify, and distribute the codes and data for personal, educational, or commercial purposes and acknowledge the project by [citing](https://github.com/ehsankazemi47/sewer_defects/blob/coudlabs/CITATION.cff) this repository. The full license can be read [here](https://github.com/ehsankazemi47/sewer_defects/blob/coudlabs/LICENSE).
