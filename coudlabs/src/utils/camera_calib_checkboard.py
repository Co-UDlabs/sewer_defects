import cv2
import numpy as np
import glob
import os

def camcalib_checkboard(CHECKERBOARD, sql, input_path):
    # Stop the iteration when specified
    # accuracy, epsilon, is reached or
    # specified number of iterations are completed.
    criteria = (cv2.TERM_CRITERIA_EPS +
                cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # Vector for 3D points
    threedpoints = []

    # Vector for 2D points
    twodpoints = []

    # 3D points real world coordinates
    objectp3d = np.zeros((1, CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
    objectp3d[0, :, :2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2) * sql
    prev_img_shape = None

    # Check if input_path is a folder or a video file
    if os.path.isdir(input_path):
        # Input path is a folder containing still images
        paths = glob.glob(os.path.join(input_path, '*.jpg'))
        
        images = []
        for filepath in paths:
            image = cv2.imread(filepath)
            images.append(image)

    else:
        # Input path is a video file
        cap = cv2.VideoCapture(input_path)
        images = []

        while cap.isOpened():
            ret, frame = cap.read()

            if not ret:
                break

            images.append(frame)

        cap.release()

    for image in images:
        grayColor = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Find the chessboard corners
        # If desired number of corners are
        # found in the image then ret = true
        ret, corners = cv2.findChessboardCorners(grayColor, CHECKERBOARD, cv2.CALIB_CB_ADAPTIVE_THRESH
                                                 + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)

        # If desired number of corners can be detected, refine the pixel coordinates
        # for given 2D points.
        if ret:
            threedpoints.append(objectp3d)

            corners2 = cv2.cornerSubPix(grayColor, corners, (11, 11), (-1, -1), criteria)
            twodpoints.append(corners2)

            # Draw and display the corners
            image = cv2.drawChessboardCorners(image, CHECKERBOARD, corners2, ret)

        cv2.imshow('img', image)
        cv2.waitKey(1)

    cv2.destroyAllWindows()

    h, w = grayColor.shape

    # Perform camera calibration by passing the value of above found out 3D points (threedpoints)
    # and its corresponding pixel coordinates of the detected corners (twodpoints)
    ret, matrix, distortion, r_vecs, t_vecs = cv2.calibrateCamera(threedpoints, twodpoints, (w, h), None, None)

    # Display the required output
    print(" Camera matrix (pixel):")
    print(matrix)

    print("\n Distortion coefficient:")
    print(distortion)

    print("\n Rotation Vectors:")
    print(r_vecs)

    print("\n Translation Vectors (m):")
    print(t_vecs)


# Define the dimensions of the checkerboard
CHECKERBOARD = (6, 9)
# Size of square on the checkerboard (length of one side) in meters
sql = 0.03  # (m)
# Path to image
file_path = "C:/Users/ci1ek/Desktop/Motion/checkboard.mp4"
# Run calibration
camcalib_checkboard(CHECKERBOARD,sql,file_path)