import sys
import os
import cv2
sys.path.append('C:/Ehsan/sewer_defects/coudlabs/src/utils')
from distance_and_size import distsize

def map(video_path, file_path_ref, file_path_other, real_size_ref, focal_length):

    # plot specs
    line_thickness = 2
    font = cv2.FONT_HERSHEY_DUPLEX
    font_scale = 0.5
    font_thickness = 1

    # Read the video
    cap = cv2.VideoCapture(video_path)

    # Get the video's frame width and height
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Create a VideoWriter object to save the output video
    output_path = os.path.join(os.path.dirname(video_path),"output.mp4")
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, 30.0, (frame_width, frame_height))

    # Read the data from the reference object's file
    with open(file_path_ref, 'r') as file_ref:
        data_ref = [line.strip().split() for line in file_ref]

    # Read the data from the other object's file
    with open(file_path_other, 'r') as file_other:
        data_other = [line.strip().split() for line in file_other]

    # Calculate the size ratios, distances, and real sizes
    distance_ref_list, distance_other_list, real_size_other_list, \
        common_frame_numbers =distsize(data_ref, data_other, real_size_ref, focal_length)
    
    # Iterate over the video frames
    frame_number = 0
    distsize_id = 0
    while cap.isOpened():       
        ret, frame = cap.read()

        if not ret:
            break

        # draw ref object box
        for i, row in enumerate(data_ref):
            if row and int(row[0]) == frame_number:
                x = float(row[1])
                y = float(row[2])
                w = float(row[3])
                h = float(row[4])
                x_ref = int(frame_width*x) - int(frame_width*w/2)
                y_ref = int(frame_height*y) - int(frame_height*h/2)
                w_ref = int(w*frame_width)
                h_ref = int(h*frame_height)
                cv2.rectangle(frame, (x_ref, y_ref), \
                    (x_ref + w_ref, y_ref + h_ref), (0, 255, 0), line_thickness)
                
        # draw other object box
        for i, row in enumerate(data_other):
            if row and int(row[0]) == frame_number:
                x = float(row[1])
                y = float(row[2])
                w = float(row[3])
                h = float(row[4])
                x_other = int(frame_width*x) - int(frame_width*w/2)
                y_other = int(frame_height*y) - int(frame_height*h/2)
                w_other = int(w*frame_width)
                h_other = int(h*frame_height)
                cv2.rectangle(frame, (x_other, y_other), \
                    (x_other + w_other, y_other + h_other), (255, 0, 0), line_thickness)
 
        # if both objects are present in the frame
        if frame_number in common_frame_numbers:

            # Box data (extracted from text files)
            #ref = [row for row in data_ref if int(row[0]) == frame_number][0]
            #other = [row for row in data_other if int(row[0]) == frame_number][0]

            # Write text with the estimated distance and real height on the image
            distance_ref = distance_ref_list[distsize_id]
            distance_other = distance_other_list[distsize_id]
            real_size_other = real_size_other_list[distsize_id]

            if distance_other is not None and real_size_other is not None:

                # write size of ref object
                text_size_ref = f"{real_size_ref:.2f} m"
                (text_width, text_height) = cv2.getTextSize(text_size_ref, font, \
                    fontScale=font_scale, thickness=font_thickness)[0]
                cv2.putText(frame, text_size_ref, (int(x_ref + w_ref), \
                    int(y_ref + h_ref - 1.1 * text_height)), \
                    font, font_scale, (0, 255, 0), font_thickness, cv2.LINE_AA)                

                # write relative distacne of other object to camera
                text_dist_other = f"{distance_other/distance_ref:.2f}"
                (text_width, text_height) = cv2.getTextSize(text_dist_other, font, \
                    fontScale=font_scale, thickness=font_thickness)[0]
                cv2.putText(frame, text_dist_other, (int(x_other + w_other), \
                    int(y_other + h_other + 0.1 * text_height)), \
                    font, font_scale, (255, 0, 0), font_thickness, cv2.LINE_AA)                
                # write size of other object
                text_size_other = f"{real_size_other:.2f} m"
                (text_width, text_height) = cv2.getTextSize(text_size_other, font, \
                    fontScale=font_scale, thickness=font_thickness)[0]
                cv2.putText(frame, text_size_other, (int(x_other + w_other), \
                    int(y_other + h_other - 1.1 * text_height)), \
                    font, font_scale, (255, 0, 0), font_thickness, cv2.LINE_AA)                

            distsize_id += 1

        # Display the frame on the screen
        cv2.imshow('Output', frame)
        cv2.waitKey(1)

        # Write the frame to the output video
        out.write(frame)

        frame_number += 1

    # Release the video capture and writer objects
    cap.release()
    out.release()
    cv2.destroyAllWindows()

    print(f"Output video saved to: {output_path}")


# Example usage
path = "C:/Ehsan/sewer_defects/coudlabs/examples/estimate size using a reference object/02/"
video_path = path + "video.mp4"
file_path_ref = path + "0.txt"
file_path_other = path + "1.txt"
real_size_ref = 0.13  # Real size of the reference object in meters
focal_length = 200  # Focal length of the camera in pixels

map(video_path, file_path_ref, file_path_other, real_size_ref, focal_length)