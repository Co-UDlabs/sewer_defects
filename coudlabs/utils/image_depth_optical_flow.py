import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

# Pipe diameter
#dia = 0.2 # (m)

# Video location
file_path = "C:/Users/ci1ek/Desktop/test/video2.mp4"
folder, filename = os.path.split(file_path)
filename, extension = os.path.splitext(filename)

# Get the video
video = cv2.VideoCapture(file_path)

# Get information about the video
fps = video.get(cv2.CAP_PROP_FPS)  # frame rate
width  = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))   # image width
height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))  # image height

# pixel size in (mm)
#ps_mm = (dia * 1000 / height)

# Empty numpy array for previous grey frame
prev_gray_frame = np.zeros((height,width))

# Create a figure to plot the output
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out_file_path = os.path.join(folder,filename,'_depth.mp4')
out = cv2.VideoWriter(out_file_path, fourcc, fps, (2 * width, height))

# Plot the original video
while True:
    # Get the frame
    ret, frame = video.read()

    # If the frame is not read successfully, break
    if not ret:
        break

    # Convert the frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Calculate the optical flow
    flow = cv2.calcOpticalFlowFarneback(gray_frame, prev_gray_frame, None, 0.5, 3, 15, 5, 3, 1.2, 0)

    # Estimate the depth
    depth = np.sqrt(np.sum(flow ** 2, axis=2))  # in pixels
    #depth_mm = depth * ps_mm  # in mm

    # Plot original frame and depth map as contour plot side by side
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
    im = ax1.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    ax1.set_title('Original Frame')
    im_depth = ax2.imshow(depth, cmap='gray')
    ax2.set_title('Depth Map')
    
    # Add colorbar to depth map plot
    divider = make_axes_locatable(ax2)
    cax = divider.append_axes('right', size='5%', pad=0.05)
    cbar = plt.colorbar(im_depth, cax=cax)
    cbar.ax.set_ylabel('Depth (pixels)')

    # Adjust layout of figure
    plt.tight_layout()
    
    # Update the figure
    fig.canvas.draw()
    plot_img = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8) \
        .reshape(fig.canvas.get_width_height()[::-1] + (3,))
    
    # Write the output frame to the output video
    out.write(plot_img)
         
    # Display the output frame on the screen
    cv2.imshow('Output Frame', plot_img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Set new frame as previous frame for the next step
    prev_gray_frame = gray_frame
    
    # close figure
    plt.close(fig)

# Close the video
video.release()
out.release()
cv2.destroyAllWindows()