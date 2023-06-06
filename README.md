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