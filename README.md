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
## Object Size Estimation Model

The Object Size Estimation model is designed to estimate the real size of an object in a video using the real size of a reference object present alongside the target object. This model also requires knowledge of the focal length of the camera, which can be estimated using the Camera Calibration model.

### Overview

The Object Size Estimation model consists of two code files:

1. `object_size.py`: This file contains the main implementation of the model. It reads a video file containing frames of objects and their respective bounding box coordinates. The model calculates the distances and sizes of objects in the video based on a reference object of known size. The calculated distances and sizes are then overlaid on the video frames and saved as an output video.

2. `distance_and_size.py`: This file contains a helper function used by `object_size.py` to calculate the size ratios, distances, and real sizes of objects. The function takes the data of the reference object, data of the other object, real size of the reference object, and focal length of the camera as input, and returns lists of estimated distances, real sizes, and common frame numbers where both objects are present.

### Usage

To use the Object Size Estimation model, follow these steps:

1. Ensure that you have the necessary dependencies installed. The required dependencies are OpenCV (`cv2`).

2. Place the `object_size.py` and `distance_and_size.py` files in the same directory.

3. Import the necessary modules and functions:

```python
import cv2
from distance_and_size import distsize_I as distsize
```

4. Use the `map` function from `object_size.py` to process the video and generate the output. Provide the paths to the input video file, reference object's data file, other object's data file, real size of the reference object, and focal length of the camera as arguments:

```python
video_path = "path/to/input_video.mp4"
file_path_ref = "path/to/reference_object_data.txt"
file_path_other = "path/to/other_object_data.txt"
real_size_ref = 0.212  # Real size of the reference object in meters
focal_length = 355  # Focal length of the camera in pixels

map(video_path, file_path_ref, file_path_other, real_size_ref, focal_length)
```

Make sure to replace `"path/to/input_video.mp4"`, `"path/to/reference_object_data.txt"`, and `"path/to/other_object_data.txt"` with the actual file paths.

### Example

Here is an example usage of the Object Size Estimation model:

```python
import cv2
from distance_and_size import distsize_I as distsize

# Specify the paths and parameters
video_path = "path/to/input_video.mp4"
file_path_ref = "path/to/reference_object_data.txt"
file_path_other = "path/to/other_object_data.txt"
real_size_ref = 0.212  # Real size of the reference object in meters
focal_length = 355  # Focal length of the camera in pixels

# Process the video and generate the output
map(video_path, file_path_ref, file_path_other, real_size_ref, focal_length)
```

Ensure that you have the video file and data files available at the specified paths.

### Notes

- Make sure to provide the correct paths to the input video file, reference object's data file, and other object's data file.

- The `real_size_ref` parameter should be the real size of the reference object in meters.

- The `focal_length` parameter should be the focal length of the camera in pixels.

- Ensure that the required modules and files are accessible by providing the correct paths