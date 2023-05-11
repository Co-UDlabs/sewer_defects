import cv2
import matplotlib.pyplot as plt
import numpy as np

# data
vid_dir = "C:/Users/ci1ek/Desktop/New folder/"
vid_name = "05-L-872-01_ICG4_SO95694504XD1_DVD1_MPEG_A_09222005_1026_28_229i.mpg"

# Define variables for calculating camera speed
prev_frame_time = 0
curr_frame_time = 0
prev_pos = None
speed = 0
frame_count = 0
npr = 5

# Create arrays to store the time and speed values
times = []
speeds = []

# Create a VideoWriter object to save the output video
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output.mp4', fourcc, 30, (1280, 720))

# Read the video file
cap = cv2.VideoCapture(vid_dir + vid_name)

# Set up the plot
fig, axs = plt.subplots(2, figsize=(5,7))

# Turn on interactive mode to update the plot in real-time
plt.ion()

# Set up the time axis for the plot
time_axis = np.linspace(0, cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0, 100)

while cap.isOpened():

    # Read a frame from the video
    ret, frame = cap.read()
    
    if ret and frame_count % npr == 0:
        
        # print frame number
        print(f'frame {frame_count}')
        
        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Apply a Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Detect edges using the Canny edge detector
        edges = cv2.Canny(blurred, 50, 150)

        # Find contours in the edges image
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Draw the contours on the original frame for visualization
        cv2.drawContours(frame, contours, -1, (0, 0, 255), 2)

        # Write `speed` value on the image
        speed_text = f'Speed: {speed:.2f} pixels per second'
        cv2.putText(frame, speed_text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

        # Calculate the position of the largest contour
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            M = cv2.moments(largest_contour)
            pos = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))
        else:
            pos = None

        # Calculate the camera speed based on the change in position and time
        if prev_pos and pos:
            curr_frame_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0
            time_diff = curr_frame_time - prev_frame_time
            pos_diff = abs(pos[0] - prev_pos[0]) + abs(pos[1] - prev_pos[1])
            speed = pos_diff / time_diff

            # Append the time and speed to the arrays for plottingq
            times.append(curr_frame_time)
            speeds.append(speed)

        # Update the previous position and time variables
        prev_pos = pos
        prev_frame_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0
        
        # Plot the current frame in the second subplot
        axs[0].imshow(frame)
        axs[0].set_xticks([])
        axs[0].set_yticks([])
        
        # Plot speed vs time
        axs[1].plot(times, speeds, '-b')
        axs[1].set_xlim(0, curr_frame_time)
        axs[1].set_xlabel('Time (s)')
        axs[1].set_ylabel('Speed (pixels per second)')

        # Pause the plot and update the display
        fig.tight_layout()
        plt.pause(0.01)
        plt.draw()

        # Write the frame to the output video file
        out.write(frame)
    
    # increase frame_count by one
    frame_count += 1

# Release the output video writer and close the window
out.release()
cv2.destroyAllWindows()