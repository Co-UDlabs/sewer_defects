import os
import cv2
import numpy as np
from tqdm import tqdm
import torch
import matplotlib.pyplot as plt

# Define the path of the input directory or file
input_path = "C:/Users/ci1ek/Desktop/New folder/09-L-872-01_SERGRD4_SO95690904XU1_DVD1_MPEG_A_09272005_1236_63_531i.mpg"

# Path to the pre-trained model
model_path = "C:/Ehsan/sewer_defects/MiDaS/pretrained_MiDaS_models/model_f46da743.pt"

# split `input_path` into directory, filename and file extension
directory = os.path.dirname(input_path)
filename = os.path.basename(input_path)
file_extension = os.path.splitext(filename)[1]

# Define the path of the output directory
output_path = os.path.join(directory,"output")

# Load the MiDaS model
model = torch.hub.load("intel-isl/MiDaS", "MiDaS")
model.load_state_dict(torch.load(model_path))  # Load the model weights
model.eval()  # Set the model to evaluation mode

# device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Define the threshold for MiDaS output
threshold = 0.5

# Define the colormap for the depth map
colormap = cv2.COLORMAP_JET

# Check if the input path is a file or directory
if os.path.isfile(input_path):
    # If input path is a file, process the file
    # Load the video
    cap = cv2.VideoCapture(input_path)
    # Get the video properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    # Create the output video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    output_filename = input_path.split("/")[-1] + "_output"
    output_video_path = os.path.join(output_path, output_filename)
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (2 * width, height))
    # Loop through each frame
    for i in tqdm(range(total_frames)):
        # Read the frame
        ret, frame = cap.read()
        if not ret:
            break
        # Resize the frame to the size required by MiDaS
        midas_input = cv2.resize(frame, (256, 256), interpolation=cv2.INTER_LINEAR)
        # Normalize the MiDaS input
        midas_input = midas_input / 255.0
        # Convert the input image to a 3D numpy array
        midas_input = np.array(midas_input)
        # Transpose the input array to match the expected shape of the model
        if len(midas_input.shape) == 2: # If grayscale image
            midas_input = np.expand_dims(midas_input, axis=2)
        midas_input = np.transpose(midas_input, (2, 0, 1))
        midas_input = torch.from_numpy(midas_input).float()
        midas_input = midas_input.unsqueeze(0)
        # Pass the tensor through the model
        midas_output = model.forward(midas_input.to(device)).squeeze().detach().cpu().numpy()
        midas_output = cv2.resize(midas_output, (width, height))
        # Threshold the MiDaS output
        th = np.uint8(midas_output > threshold)
        # Apply the colormap to the thresholded output
        depth_map = cv2.applyColorMap(th, colormap)
        # Combine the original frame and the depth map
        output_frame = np.concatenate((frame, depth_map), axis=1)
        # Display the output frame
        cv2.imshow("Output", output_frame)   
        cv2.waitKey(0.01)     
        # Write the frame to the output video
        out.write(output_frame)

    # Release the video and output video writers
    cap.release()
    out.release()
else:
    # If input path is a directory, process all images in the directory
    # Loop through
    # Create the output directory if it does not exist
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Loop through each file in the directory
    for filename in os.listdir(input_path):
        # Check if the file is an image
        if filename.endswith(('.jpg', '.jpeg', '.png', '.bmp')):
            # Load the image
            img_path = os.path.join(input_path, filename)
            img = cv2.imread(img_path)

            # Resize the image to the size required by midas
            midas_input = cv2.resize(img, (256, 256))

            # Normalize the midas input
            midas_input = midas_input / 255.0

            # Convert the midas input to a tensor
            midas_input = np.expand_dims(midas_input, axis=0)
            midas_input = np.transpose(midas_input, (0, 3, 1, 2))
            midas_input = torch.from_numpy(midas_input).float()

            # Pass the midas input through the model to get the depth map
            with torch.no_grad():
                depth = model(midas_input)

            # Convert the depth map to a numpy array
            depth = depth.squeeze().cpu().numpy()

            # Normalize the depth map
            depth = (depth - depth.min()) / (depth.max() - depth.min())

            # Convert the depth map to a color map
            cmap = plt.get_cmap('magma')
            depth_color = cmap(depth)
            depth_color = (depth_color[:, :, :3] * 255).astype(np.uint8)

            # Stack the original image and the depth map together
            result = np.hstack((img, depth_color))

            # Save the result
            output_filename = os.path.splitext(filename)[0] + "_output.png"
            output_pathname = os.path.join(output_path, output_filename)
            cv2.imwrite(output_pathname, result)

        # Check if the file is a video
        elif filename.endswith(('.mp4', '.avi', '.mov')):
            # Load the video
            video_path = os.path.join(input_path, filename)
            cap = cv2.VideoCapture(video_path)

            # Get the video properties
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

            # Create the output video writer
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            output_filename = os.path.splitext(filename)[0] + "_output.mp4"
            output_pathname = os.path.join(output_path, output_filename)
            out = cv2.VideoWriter(output_pathname, fourcc, fps, (2*width, height))

            # Loop through each frame
            for i in tqdm(range(total_frames)):
                # Read the frame
                ret, frame = cap.read()
                if not ret:
                    break

                # Resize the frame to the size required by midas
                midas_input = cv2.resize(frame, (256, 256))

                # Normalize the midas input
                midas_input = midas_input / 255.0

                # Convert the midas input to a tensor
                #midas_input = np.expand_dims(midas_input, axis=0)
                #midas_input = np.transpose(midas_input, (0, 3, 1, 2))
                #midas_input = torch.from_numpy(m
    
                # Convert the midas input to a tensor
                midas_input = torch.from_numpy(midas_input)
                midas_input = midas_input.to(device)
                midas_input = midas_input.unsqueeze(0)

                # Run the model on the input
                with torch.no_grad():
                    prediction = model(midas_input)

                # Convert the output tensor to a numpy array
                depth_map = prediction.squeeze().cpu().numpy()

                # Normalize the depth map for visualization
                depth_map = (depth_map - np.min(depth_map)) / (np.max(depth_map) - np.min(depth_map))

                # Convert the depth map to a color map for visualization
                depth_map_color = cv2.applyColorMap((depth_map * 255).astype(np.uint8), cv2.COLORMAP_JET)

                # Concatenate the input and output images horizontally
                output_image = np.concatenate([img, depth_map_color], axis=1)

                # Write the output image to the output directory
                output = os.path.join(output_path, f"{filename}_output.jpg")
                cv2.imwrite(output, output_image)

print("Processing complete.")
