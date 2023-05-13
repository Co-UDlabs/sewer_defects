import cv2
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

# Load video file
data_path = "C:/Users/ci1ek/Desktop/test/IMG_9028.MOV"
cap = cv2.VideoCapture(data_path)

# Set output video parameters
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output_video.mp4', fourcc, fps, (2 * frame_width, frame_height))

# Define image processing function
def process_frame(frame):
    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply Canny edge detection to extract edges
    thresh = 100
    edges = cv2.Canny(gray, int(0.35*thresh), thresh)

    # Apply Hough transform to extract lines
    lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi/180, \
        threshold=int(0.35*thresh), minLineLength=10, maxLineGap=5)

    # Create blank image for depth map
    depth_map = np.zeros_like(gray)

    # Iterate over all detected lines
    for line in lines:
        x1, y1, x2, y2 = line[0]
        # Draw line on depth map with thickness proportional to line length
        cv2.line(depth_map, (x1, y1), (x2, y2), (255, 255, 255), \
            thickness=int(np.sqrt((x2 - x1)**2 + (y2 - y1)**2)))

    return depth_map

# Loop through each frame
while(cap.isOpened()):
    # Read the frame
    ret, frame = cap.read()
    if not ret:
        break

    # Process the frame to obtain depth map
    depth_map = process_frame(frame)

    # Plot original frame and depth map as contour plot side by side
    fig, ax = plt.subplots(1, 2, figsize=(10, 5))
    im = ax[0].imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    ax[0].set_title('Original Frame')
    im_depth = ax[1].imshow(depth_map, cmap='jet')
    ax[1].set_title('Depth Map')
    
    # Add colorbar to depth map plot
    divider = make_axes_locatable(ax[1])
    cax = divider.append_axes('right', size='5%', pad=0.05)
    cbar = plt.colorbar(im_depth, cax=cax)
    cbar.ax.set_ylabel('Depth (pixels)')

    # Adjust layout of figure
    plt.tight_layout()
    
    # Convert plot to image and concatenate with original frame
    fig.canvas.draw()
    plot_img = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8) \
        .reshape(fig.canvas.get_width_height()[::-1] + (3,))

    # Write the output frame to the output video
    out.write(plot_img)

    # Display the output frame on the screen
    cv2.imshow('Output Frame', plot_img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
out.release()
cv2.destroyAllWindows()