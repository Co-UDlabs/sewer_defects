# Sewer Defects Processing Project

Welcome to the Sewer Defects Processing Project! This project focuses on processing CCTV images of sewer pipes to detect defects, calibrate cameras, and estimate object sizes. It utilizes deep learning models and computer vision techniques to provide accurate results.

## Project Structure

The project has the following structure:

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
¦   ¦       +-- object_size.ipynb
¦   ¦       +-- object_size.py
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
¦   ¦       +-- __init__.py
¦   ¦       +-- distance_and_size.py
¦   ¦       +-- object_size.py
¦   +-- trained_models/
+-- ultralytics/
    +-- assets/
    +-- models/
    +-- yolo/
    +-- tracker/
    +-- hub/
    +-- nn/


In the above structure, the `ultralytics` directory contains the YOLO model implementation, while the `cloudlabs` directory contains the source code, data, and examples for the Sewer Defects Processing Project.

## Functionalities

### 1. Defect Detection

The main functionality of the project is to detect defects in sewer pipes using the YOLO v8 model implemented by Ultralytics. The defect detection model is trained using labeled images of sewer defects. You can follow these steps to use the defect detection model:

1. Collect images of sewer defects and label them using the [YoloLabel](https://github.com/developer0hye/Yolo_Label) tool. Categorize the defects as 'obstacle - Block', 'obstacle - deposit', 'obstacle - tree root', 'joint', 'crack', 'damage - hole', 'damage - severe', or 'corrosion'.

2. Organize the labeled images and labels in a folder named 'data' or 'sewer defect data'. Create a subfolder named 'labelled_images' and place the images and label files inside it.

3. Use the `check_data.ipynb` notebook or the `check_data.py` script provided in the `examples/defect_detection_examples` directory to verify the data and ensure it is correctly labeled.

4. Prepare the data for model training by running the `prepare_data.ipynb` notebook or the `prepare_data.py` script in the `examples/defect_detection_examples` directory. This process will split the data into training, validation, and test subsets and copy them into the `data` folder under `cloudlabs`. Additionally, you need to modify the `data.yaml` file in the `data` folder to specify the dataset configuration.

5. Train and test the defect detection model using the `train_and_test.ipynb` notebook in the `examples/defect_detection_examples` directory. The trained models will be saved under `cloudlabs/trained_models`.

6. To detect defects in unseen images, use the `detect_unseen.ipynb` notebook in the `examples/defect_detection_examples` directory. This notebook demonstrates how to load the trained model and perform defect detection on new images.

### 2. Camera Calibration

The project includes modules for calibrating a camera, which is useful when the specifications, especially the focal length, of the camera are unknown. There are two methods available: Checkerboard and Box calibration.

- **Checkerboard Calibration**: If you have an image of a checkerboard recorded by the camera, you can use the `calib_checkerboard.ipynb` notebook in the `examples/camera_calibration_examples` directory to calibrate the camera. This method handles both videos and groups of still images.

- **Box Calibration**: If a checkerboard image is not available, you can use the `calib_box.ipynb` notebook in the `examples/camera_calibration_examples` directory. This method involves labeling an object with a known size (e.g., a box) and using images of the object from different distances to calibrate the camera. This method also works with videos and groups of still images.

Both calibration methods output a calibration matrix, which includes the focal length and other camera parameters.

### 3. Object Size Estimation

The object size estimation module allows you to estimate the size of objects in sewer pipe images. Here's how you can use it:

1. **Focal Length Determination**: Before estimating object sizes, you need to determine the focal length of the camera used to capture the images. This information is crucial for accurate size estimation.

2. **Reference Object Selection**: Identify a reference object in the sewer pipe images with a known size. Joints in CCTV images of sewer pipes are commonly used as reference objects.

3. **Size Estimation**: Run the `object_size.ipynb` notebook in the `examples/object_size_estimation_examples` directory. This notebook demonstrates how to estimate the size of objects based on the known size of the reference object and the camera's focal length.

## Data and Examples

For detailed examples on how to use the Sewer Defects Processing Project, please refer to the [`examples`](./examples) directory in the repository. It contains step-by-step notebooks and scripts for defect detection, camera calibration, and object size estimation.

## License

This project is licensed under the [MIT License](./LICENSE). Feel free to use and modify the code according to your needs.

Feel free to copy the above content and use it as your README.md file for your GitHub repository.