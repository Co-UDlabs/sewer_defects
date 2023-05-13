import numpy as np
import cv2
import glob

# input image
data_dir = "C:/Users/ci1ek/Desktop/New folder/"
image_name = "14_15_calib_newcam_WMH3_west_forward_twice_210610_1420A-Survey"

# Define the number of corners in the calibration pattern
num_corners = (9, 6)

# Create a grid of object points based on the number of corners
objp = np.zeros((num_corners[0] * num_corners[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:num_corners[0], 0:num_corners[1]].T.reshape(-1, 2)

# Create empty lists to store object points and image points from all calibration frames
obj_points = []
img_points = []

# Iterate through all calibration images and detect corners
calibration_images = glob.glob(data_dir+image_name+"/*.jpg")
for calibration_image in calibration_images:
    # Load the calibration image
    img = cv2.imread(calibration_image)

    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Find the chessboard corners in the grayscale image
    ret, corners = cv2.findChessboardCorners(gray, num_corners, None)

    # If corners are found, add object points and image points to their respective lists
    if ret == True:
        obj_points.append(objp)
        img_points.append(corners)

        # Display the image with detected corners
        cv2.drawChessboardCorners(img, num_corners, corners, ret)
        cv2.imshow("Calibration", img)
        cv2.waitKey(500)

# Use the object points and image points to calibrate the camera
ret, camera_matrix, distortion_coefficients, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points, gray.shape[::-1], None, None)

# Save the camera matrix and distortion coefficients to files
np.save(data_dir+image_name+"_camera_matrix.npy", camera_matrix)
np.save(data_dir+image_name+"_distortion_coefficients.npy", distortion_coefficients)

# Destroy the window
cv2.destroyAllWindows()