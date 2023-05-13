import torch
import cv2
import numpy as np
from monodepth2 import *
import sys
sys.path.insert(0, 'C:/Ehsan/sewer_defects/monodepth2/')
from options import MonodepthOptions

# Load video file
data_path = "C:/Users/ci1ek/Desktop/test/video.mp4"
cap = cv2.VideoCapture(data_path)

# Set output video parameters
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output_video.mp4', fourcc, fps, (2 * frame_width, frame_height))

# Load model
model_path = download_model_if_doesnt_exist("mono_640x192")
model = Monodepth2Model(model_path)
model.eval()
device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
model.to(device)

# Loop through each frame
while(cap.isOpened()):
    # Read the frame
    ret, frame = cap.read()
    if not ret:
        break

    # Convert frame to tensor
    frame_tensor = torch.from_numpy(frame).to(device).unsqueeze(0).float() / 255.0

    # Predict depth map
    with torch.no_grad():
        depth = model(frame_tensor)

    # Convert depth map to grayscale and resize to original frame size
    depth_map = cv2.resize(depth.squeeze().cpu().numpy(), (frame_width, frame_height))
    depth_map = cv2.cvtColor((depth_map / depth_map.max() * 255).astype(np.uint8), cv2.COLOR_GRAY2BGR)

    # Concatenate original frame and depth map horizontally
    output_frame = np.concatenate((frame, depth_map), axis=1)

    # Write the output frame to the output video
    out.write(output_frame)

    # Display the output frame on the screen
    cv2.imshow('Output Frame', output_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
out.release()
cv2.destroyAllWindows()
