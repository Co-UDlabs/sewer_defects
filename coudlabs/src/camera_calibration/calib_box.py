'''
File name: camera_calib_box.py
Author: Ehsan Kazemi
Date created: May 2023
Date last modified: 06/06/2023
-------------------------------------------------------------------------
This code checks if the input_path is a folder or a video file. If it's
a folder, it will read the images and corresponding label information
from a text file. If it's a video file, it will read the video frames
and corresponding label information from a text file. The rest of the
code performs camera calibration using OpenCV.
-------------------------------------------------------------------------
'''

import os
import cv2
import numpy as np
import pandas as pd

def plot_box_on_image(image, corners_pixel):
    # Draw lines connecting the corners
    corners_pixel = corners_pixel.astype(np.int32)
    cv2.polylines(image, [corners_pixel], isClosed=True, color=(0, 255, 0), thickness=2)

    # Draw circles at the corners
    for corner in corners_pixel:
        cv2.circle(image, tuple(corner), radius=3, color=(0, 255, 0), thickness=-1)

    # Display the image
    cv2.imshow("Image", image)
    cv2.waitKey(1)

def calibrate_camera_with_box(input_path, object_width, object_height):
        
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input path '{input_path}' does not exist.")

    if not os.path.isfile(input_path) and not os.path.isdir(input_path):
        raise ValueError(f"Input path '{input_path}' is neither a file nor a directory.")

    # Prepare object points (grid) for the rectangular object
    # It is always the same for all the images since the real size of the object is fixed
    object_points = np.zeros((4, 3), dtype=np.float32)
    object_points[:, :2] = np.array([[0, 0], [object_width, 0],
                                     [0, object_height], [object_width, object_height]])

    # Arrays to store object points and image points from all calibration frames
    object_points_list = []
    image_points_list = []

    # Check if input_path is a folder or a video file
    if os.path.isdir(input_path):
        # Input path is a folder containing still images and a text file
        txt_file = os.path.join(input_path, 'box_coordinates.txt')

        # Read the labels from the text file
        labels = pd.read_csv(txt_file, sep=" ", header=None)
        labels.columns = ["filename", "x0", "y0", "width", "height"]

        for index, label in labels.iterrows():
            # Extract corner information from the text file
            image_name = label["filename"]
            image_path = os.path.join(input_path, image_name)

            # Load the image
            image = cv2.imread(image_path)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Calculate the image dimensions
            image_height, image_width = image.shape[:2]

            # Calculate the image points (2D points) in pixels
            box_center_x = label["x0"]  # Relative position of the box's center along the x-axis (0.0 to 1.0)
            box_center_y = label["y0"]  # Relative position of the box's center along the y-axis (0.0 to 1.0)
            box_width = label["width"]  # Relative width of the box (0.0 to 1.0)
            box_height = label["height"]  # Relative height of the box (0.0 to 1.0)
            corners_pixel = np.float32([
                [(box_center_x - box_width / 2) * image_width, (box_center_y - box_height / 2) * image_height],
                [(box_center_x + box_width / 2) * image_width, (box_center_y - box_height / 2) * image_height],
                [(box_center_x + box_width / 2) * image_width, (box_center_y + box_height / 2) * image_height],
                [(box_center_x - box_width / 2) * image_width, (box_center_y + box_height / 2) * image_height]])

            # Plot corners on the image
            plot_box_on_image(image, corners_pixel)

            # Store the object points and image points
            object_points_list.append(object_points)
            image_points_list.append(corners_pixel)

    elif os.path.isfile(input_path):
        # Input path is a video file
        txt_file = os.path.join(os.path.dirname(input_path), 'box_coordinates.txt')
        labels = pd.read_csv(txt_file, sep=" ", header=None)
        labels.columns = ["frame", "x0", "y0", "width", "height"]

        # Open the video file
        cap = cv2.VideoCapture(input_path)

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Get the current frame number
            frame_number = int(cap.get(cv2.CAP_PROP_POS_FRAMES))

            # Find the corresponding label for the current frame
            label = labels[labels["frame"] == frame_number]

            if not label.empty:
                # Calculate the image dimensions
                image_height, image_width = frame.shape[:2]

                # Calculate the image points (2D points) in pixels
                box_center_x = label["x0"].iloc[0]  # Relative position of the box's center along the x-axis (0.0 to 1.0)
                box_center_y = label["y0"].iloc[0]  # Relative position of the box's center along the y-axis (0.0 to 1.0)
                box_width = label["width"].iloc[0]  # Relative width of the box (0.0 to 1.0)
                box_height = label["height"].iloc[0]  # Relative height of the box (0.0 to 1.0)
                corners_pixel = np.float32([
                    [(box_center_x - box_width / 2) * image_width, (box_center_y - box_height / 2) * image_height],
                    [(box_center_x + box_width / 2) * image_width, (box_center_y - box_height / 2) * image_height],
                    [(box_center_x + box_width / 2) * image_width, (box_center_y + box_height / 2) * image_height],
                    [(box_center_x - box_width / 2) * image_width, (box_center_y + box_height / 2) * image_height]])

                # Plot corners on the image
                plot_box_on_image(frame, corners_pixel)

                # Store the object points and image points
                object_points_list.append(object_points)
                image_points_list.append(corners_pixel)

        # Release the video capture object
        cap.release()
        cv2.destroyAllWindows()

    else:
        raise Exception("Invalid input path.")

    # Perform camera calibration using OpenCV
    ret, camera_matrix, distortion_coeffs, _, _ = cv2.calibrateCamera(
        object_points_list, image_points_list, gray.shape[::-1], None, None)

    # Print the calibration results
    print("\nCamera Matrix:")
    print(camera_matrix)
    print("\nDistortion Coefficients:")
    print(distortion_coeffs)
