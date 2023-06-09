"""
File name: object_size.py
Author: Ehsan Kazemi
Date created: Apr 2023
Date last modified: 05/06/2023
-------------------------------------------------------------------------\
This code processes a video file containing frames of objects and their  /
respective bounding box coordinates. It calculates the distances and     \
sizes of objects in the video based on a reference object of known size. /
The calculated distances and sizes are then overlaid on the video frames \
and saved as an output video.                                            /
...                                                                      \
The code performs the following steps:                                   /
1. Imports necessary libraries and modules.                              \
2. Defines the necessary variables and parameters for plotting           /
   specifications and video processing.                                  \
3. Reads the input video file and extracts its frame width and height.   /
4. Creates an output video file to save the processed frames.            \
5. Reads the data from the reference object's file and the other         /
   object's file.                                                        \
6. Calls the 'distsize' function from the 'distance_and_size' module to  /
   calculate the size ratios, distances, and real sizes of objects.      \
7. Iterates over the video frames and performs the following tasks:      /
   - Draws bounding boxes around the reference object and the other      \
     object on each frame.                                               /
   - Writes text on the frames indicating the estimated distances and    \
     real sizes of the objects.                                          /
   - Displays the frames on the screen.                                  \
   - Writes the frames to the output video.                              /
8. Releases the video capture and writer objects, and closes any open    \
   windows.                                                              /
9. Prints the path where the output video is saved.                      \
...                                                                      /
Example usage:                                                           \
- Provide the paths to the input video file, reference object's file,    /
  and other object's file.                                               \
- Specify the real size of the reference object and the focal length of  /
  the camera.                                                            \
- Call the 'mapp' function with the provided arguments to process the     /
  video and generate the output.                                         \
...                                                                      /
Note: Ensure that the required modules and files are accessible by       \
      providing the correct paths.                                       /
-------------------------------------------------------------------------\
"""

# Import dependencies
import sys
import os
import cv2

# Import 'distsize' function
from .distance_and_size import distsize_I as distsize

def mapp(video_path, file_path_ref, file_path_other, real_size_ref, focal_length):
    """
    Maps the reference object and other object in a video, calculates distances and sizes, and saves the output video.

    Parameters:
    - video_path: The path to the input video.
    - file_path_ref: The path to the reference object's data file.
    - file_path_other: The path to the other object's data file.
    - real_size_ref: The real size of the reference object in meters.
    - focal_length: The focal length of the camera in pixels.
    """

    # Plot specifications
    line_thickness = 2  # Thickness of the bounding box lines
    font = cv2.FONT_HERSHEY_DUPLEX  # Font style for text overlay
    font_scale = 0.5  # Font scale for text overlay
    font_thickness = 1  # Thickness of the font strokes

    # Check if the input paths exist
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")
    if not os.path.exists(file_path_ref):
        raise FileNotFoundError(f"Reference object's data file not found: {file_path_ref}")
    if not os.path.exists(file_path_other):
        raise FileNotFoundError(f"Other object's data file not found: {file_path_other}")

    # Read the video
    cap = cv2.VideoCapture(video_path)

    # Get the video's frame width and height
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Get the input file name without extension
    folder, file_name = os.path.split(video_path)
    file_name, _ = os.path.splitext(file_name)

    # Create a VideoWriter object to save the output video
    output_path = os.path.join(folder, file_name+"_output.mp4")
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, 30.0, (frame_width, frame_height))

    # Read the data from the reference object's file
    with open(file_path_ref, 'r') as file_ref:
        data_ref = [line.strip().split() for line in file_ref]

    # Read the data from the other object's file
    with open(file_path_other, 'r') as file_other:
        data_other = [line.strip().split() for line in file_other]

    # Calculate the size ratios, distances, and real sizes
    distance_ref_list, distance_other_list, real_size_other_list, common_frame_numbers = distsize(data_ref, data_other, real_size_ref, focal_length)

    # Iterate over the video frames
    frame_number = 0
    distsize_id = 0
    estimated_size = 0
    nn = 0
    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break

        # Draw the reference object box
        for i, row in enumerate(data_ref):
            if row and int(row[0]) == frame_number:
                x = float(row[1])  # x-coordinate of the object's center
                y = float(row[2])  # y-coordinate of the object's center
                w = float(row[3])  # width of the object
                h = float(row[4])  # height of the object
                x_ref = int(frame_width*x) - int(frame_width*w/2)  # x-coordinate of the top-left corner of the bounding box
                y_ref = int(frame_height*y) - int(frame_height*h/2)  # y-coordinate of the top-left corner of the bounding box
                w_ref = int(w*frame_width)  # width of the bounding box
                h_ref = int(h*frame_height)  # height of the bounding box
                cv2.rectangle(frame, (x_ref, y_ref), (x_ref + w_ref, y_ref + h_ref), (0, 255, 0), line_thickness)

        # Draw the other object box
        for i, row in enumerate(data_other):
            if row and int(row[0]) == frame_number:
                x = float(row[1])  # x-coordinate of the object's center
                y = float(row[2])  # y-coordinate of the object's center
                w = float(row[3])  # width of the object
                h = float(row[4])  # height of the object
                x_other = int(frame_width*x) - int(frame_width*w/2)  # x-coordinate of the top-left corner of the bounding box
                y_other = int(frame_height*y) - int(frame_height*h/2)  # y-coordinate of the top-left corner of the bounding box
                w_other = int(w*frame_width)  # width of the bounding box
                h_other = int(h*frame_height)  # height of the bounding box
                cv2.rectangle(frame, (x_other, y_other), (x_other + w_other, y_other + h_other), (255, 0, 0), line_thickness)

        # if both objects are present in the frame
        if frame_number in common_frame_numbers:

            # Write text with the estimated distance and real height on the image
            distance_ref = distance_ref_list[distsize_id]  # distance of the reference object to the camera
            distance_other = distance_other_list[distsize_id]  # distance of the other object to the camera
            real_size_other = real_size_other_list[distsize_id]  # real size of the other object

            if distance_other is not None and real_size_other is not None:

                # write distance of ref object to camera
                text_dist_ref = f"{distance_ref:.2f} m"
                (text_width, text_height) = cv2.getTextSize(text_dist_ref, font, fontScale=font_scale, thickness=font_thickness)[0]
                cv2.putText(frame, text_dist_ref, (int(x_ref + 1.05*w_ref), int(y_ref + 1 * text_height)), font, font_scale, (0, 255, 0), font_thickness, cv2.LINE_AA)

                # write size of ref object
                text_size_ref = f"{real_size_ref:.2f} m"
                (text_width, text_height) = cv2.getTextSize(text_size_ref, font, fontScale=font_scale, thickness=font_thickness)[0]
                cv2.putText(frame, text_size_ref, (int(x_ref + 1.05*w_ref), int(y_ref + 2.25 * text_height)), font, font_scale, (0, 255, 0), font_thickness, cv2.LINE_AA)

                # write distance of other object to camera
                text_dist_other = f"{distance_other:.2f} m"
                (text_width, text_height) = cv2.getTextSize(text_dist_other, font, fontScale=font_scale, thickness=font_thickness)[0]
                cv2.putText(frame, text_dist_other, (int(x_other + 1.05*w_other), int(y_other + h_other + 0.1 * text_height)), font, font_scale, (255, 0, 0), font_thickness, cv2.LINE_AA)

                # write size of other object
                text_size_other = f"{real_size_other:.2f} m"
                (text_width, text_height) = cv2.getTextSize(text_size_other, font, fontScale=font_scale, thickness=font_thickness)[0]
                cv2.putText(frame, text_size_other, (int(x_other + 1.05*w_other), int(y_other + h_other - 1.15 * text_height)), font, font_scale, (255, 0, 0), font_thickness, cv2.LINE_AA)

                estimated_size = estimated_size + real_size_other
                nn += 1
                
            distsize_id += 1

        # Display the frame on the screen
        cv2.imshow('Output', frame)
        cv2.waitKey(1)

        # Write the frame to the output video
        out.write(frame)

        frame_number += 1

        # Check if distsize_id exceeds the list lengths
        if distsize_id >= len(distance_ref_list) or distsize_id >= len(distance_other_list) or distsize_id >= len(real_size_other_list):
            break

    # Release the video capture and writer objects
    cap.release()
    out.release()
    cv2.destroyAllWindows()

    estimated_size = estimated_size / nn
    print(f"Estimated size of the object: {estimated_size:.2f} m")
    print(f"Output video saved to: {output_path}")
