# Camera Calibration Models

This repository contains two camera calibration models: the **Box Model** and the **Checkerboard Model**. These models are used to calibrate a camera using images or video frames.

## Box Model

The Box Model performs camera calibration by using images of a an object (like a joint inside sewer pipe) with a box drawn around it. The dimensions of the object (width and height) need to be provided as inputs. The calibration process involves the following steps:

1. Read the images and corresponding label information from a text file (if input is a folder) or a video file (if input is a video).
2. Extract the corner information from the label file and calculate the image points (2D points) in pixels.
3. Plot the corners on the image to visualize the detected corners.
4. Store the object points (grid) and image points for all calibration frames.
5. Perform camera calibration using OpenCV's `calibrateCamera` function.
6. Print the camera matrix and distortion coefficients obtained from the calibration process.

### Usage

To use the Box Model, you need to provide the following inputs:

- `input_path`: The path to the folder containing still images or the video file.
- `object_width`: The width of the rectangular object in real-world units.
- `object_height`: The height of the rectangular object in real-world units.

Make sure to have a text file named `box_coordinates.txt` in the same directory as the images or the video file. The text file should contain the label information for each image or video frame in the format: `filename x0 y0 width height`. Each line represents one frame, where:
- `filename`: The name of the image file or the frame number of the video.
- `x0`: Relative position of the box's center along the x-axis (0.0 to 1.0).
- `y0`: Relative position of the box's center along the y-axis (0.0 to 1.0).
- `width`: Relative width of the box (0.0 to 1.0).
- `height`: Relative height of the box (0.0 to 1.0).

Run the `calibrate_camera_with_box` function, passing the required inputs, to perform camera calibration.

## Checkerboard Model

The Checkerboard Model performs camera calibration using a checkerboard pattern. The calibration process involves the following steps:

1. Find the checkerboard corners in the input images or video frames.
2. Refine the pixel coordinates for the detected corners.
3. Draw and display the detected corners on the images or video frames.
4. Store the 3D points (real-world coordinates) and 2D points (pixel coordinates) for all detected corners.
5. Perform camera calibration using OpenCV's `calibrateCamera` function.
6. Print the camera matrix, distortion coefficients, rotation vectors, and translation vectors obtained from the calibration process.

### Usage

To use the Checkerboard Model, you need to provide the following inputs:

- `CHECKERBOARD`: A tuple representing the number of inner corners in the checkerboard pattern (e.g., `(9, 6)` for a 9x6 pattern).
- `sql`: The size of one square in the checkerboard pattern in real-world units.
- `input_path`: The path to the folder containing still images or the video file.

If the input is a folder, the model will look for images with the `.jpg` extension in the specified folder. If the input is a video file, the model will process the video frames.

Run the `camcalib_checkerboard` function, passing the required inputs, to perform camera calibration.

## Examples

To see examples of how to run these models, refer to the provided

 with cutoff of 4096 characters
 
 

--------------------------------------------
# Object Size Estimation Model

The Object Size Estimation model is designed to estimate the real size of an object in a video based on the real size of a reference object present alongside it. The model requires the focal length of the camera to be known, which can be estimated using the Camera Calibration model.

## Usage

The model consists of two main components:

1. `object_size.py`: This script processes a video file containing frames of objects and their respective bounding box coordinates. It calculates the distances and sizes of objects in the video based on a reference object of known size. The calculated distances and sizes are then overlaid on the video frames and saved as an output video.

2. `distance_and_size.py`: This module provides the necessary functions to calculate the size ratios, distances, and real sizes of objects based on the reference object's height and the camera's focal length.

## Example Usage

To use the Object Size Estimation model, you can follow the steps below:

1. Prepare the required input files:
   - Input video file: A video file containing frames of objects and their bounding box coordinates.
   - Reference object's data file: A text file containing data about the reference object, including frame numbers and bounding box coordinates.
   - Other object's data file: A text file containing data about the other object, including frame numbers and bounding box coordinates.

2. Install the necessary dependencies:
   - OpenCV: `pip install opencv-python`

3. Run the model using the provided examples:
   - Example 1: Jupyter Notebook
     - The notebook example demonstrates how to use the Object Size Estimation model in a step-by-step manner.
     - Download examplar data from [this Google Drive link](https://drive.google.com/drive/u/1/folders/13TPH52FVjIPhvE-GOP4AAmp0haUrH8_z) (where a video and two text files are stored) and place them in a folder on your local machine. The video shows two object, the larger one is the reference object with known height, and the smaller one is the target object of which height is to be estimated. The text files contain coordinates of the bounding boxes around the objects at frames where the boxes are present.
     - Use the notebook example at [notebook.ipynb](https://github.com/ehsankazemi47/sewer_defects/tree/documentation/coudlabs/examples/object_size_estimation_examples/notebook.ipynb) and set `folder` to where you have put the data on your local machine.
     - Run the notebook. A video will be saved in the same folder with the estimated size of the target object and its distance to the camera displayed on the image.

   - Example 2: GUI Application
     - The GUI example provides a user-friendly interface for running the Object Size Estimation model.
     - Download examplar data from [this Google Drive link](https://drive.google.com/drive/u/1/folders/13TPH52FVjIPhvE-GOP4AAmp0haUrH8_z) (where a video and two text files are stored) and place them in a folder on your local machine. The video shows two object, the larger one is the reference object with known height, and the smaller one is the target object of which height is to be estimated. The text files contain coordinates of the bounding boxes around the objects at frames where the boxes are present.
     - Run the gui.exe file in the folder [gui](https://github.com/ehsankazemi47/sewer_defects/tree/documentation/coudlabs/examples/object_size_estimation_examples/gui)
     - Set the location of the data files and specify the real size of the reference object and the focal length of the camera in the gui window and press the run the model button. A video will be saved in the same folder with the estimated size of the target object and its distance to the camera displayed on the image.

## License

This project is licensed under the [License](LICENSE).
