import cv2
import numpy as np
import glob
import os

def camcalib_checkerboard(CHECKERBOARD, sql, input_path):
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

        if not paths:
            raise ValueError("No image files found in the specified folder.")

        images = []
        for filepath in paths:
            image = cv2.imread(filepath)
            images.append(image)

    elif os.path.isfile(input_path):
        # Input path is a video file
        cap = cv2.VideoCapture(input_path)

        if not cap.isOpened():
            raise ValueError("Could not open the video file.")

        images = []

        # Initialize width and height
        w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        while cap.isOpened():
            ret, frame = cap.read()

            if not ret:
                break

            images.append(frame)

        cap.release()

    else:
        raise ValueError("The specified input_path does not exist.")

    # Get the input file name without extension
    folder, file_name = os.path.split(input_path)
    file_name, _ = os.path.splitext(file_name)

    # Create the output video file name
    output_file_name = os.path.join(folder, f"{file_name}_output.mp4")

    # Get the video codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    output_video = cv2.VideoWriter(output_file_name, fourcc, 30.0, (w, h))

    for image in images:
        grayColor = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Find the checkerboard corners
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

        output_video.write(image)

    output_video.release()
    cv2.destroyAllWindows()

    h, w = grayColor.shape

    # Perform camera calibration by passing the value of above found out 3D points (threedpoints)
    # and its corresponding pixel coordinates of the detected corners (twodpoints)
    ret, matrix, distortion, r_vecs, t_vecs = \
        cv2.calibrateCamera(threedpoints, twodpoints, (w, h), None, None)

    # Display the required output
    print(" Camera matrix (pixel):")
    print(matrix)

    print("\n Distortion coefficient:")
    print(distortion)

    print("\n Rotation Vectors:")
    print(r_vecs)

    print("\n Translation Vectors (m):")
    print(t_vecs)