import numpy as np
import cv2

# input video
vid_dir = "C:/Users/ci1ek/Desktop/New folder/"
vid_name = "14_15_calib_newcam_WMH3_west_forward_twice_210610_1420A-Survey - calibre.mp4"

# Define the number of corners in the calibration pattern
num_corners = (9, 6)

# Create a grid of object points based on the number of corners
objp = np.zeros((num_corners[0] * num_corners[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:num_corners[0], 0:num_corners[1]].T.reshape(-1, 2)

# Create empty lists to store object points and image points from all calibration frames
obj_points = []
img_points = []

# Open the video file and read the first frame
video_capture = cv2.VideoCapture(vid_dir+vid_name)
ret, frame = video_capture.read()
frame_num = 0

# Iterate through all frames in the video and detect corners
while ret == True:
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Find the chessboard corners in the grayscale frame
    ret, corners = cv2.findChessboardCorners(gray, num_corners, None)

    # If corners are found, add object points and image points to their respective lists
    if ret == True:
        obj_points.append(objp)
        img_points.append(corners)

    # Display the frame with detected corners
    cv2.drawChessboardCorners(frame, num_corners, corners, ret)
    cv2.imshow("Calibration", frame)
    cv2.waitKey(1)

    # Read the next frame
    ret, frame = video_capture.read()
    frame_num += 1

# Use the object points and image points to calibrate the camera
ret, camera_matrix, distortion_coefficients, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points, gray.shape[::-1], None, None)

# Save the camera matrix and distortion coefficients to files
np.save(vid_dir+"camera_matrix.npy", camera_matrix)
np.save(vid_dir+"distortion_coefficients.npy", distortion_coefficients)

# Close the video capture and destroy the window
video_capture.release()
cv2.destroyAllWindows()