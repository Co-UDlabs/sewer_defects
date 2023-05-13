import cv2
import numpy as np
import matplotlib.pyplot as plt

# input video
vid_dir = "C:/Users/ci1ek/Desktop/New folder/"
vid_name = "5A_midcrawler_MH4_210610_1149A-Survey.avi"

# read input video
cap = cv2.VideoCapture(vid_dir+vid_name)

# get frame dimensions
ret, frame1 = cap.read()
prev_gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
height, width = prev_gray.shape[:2]

# initialize variables
speed_list = []
time_list = []
frame_count = 0

# set parameters for Farneback method
pyr_scale = 0.5
levels = 3
winsize = 15
iterations = 3
poly_n = 5
poly_sigma = 1.1
flags = 0

# create output video writer
out = cv2.VideoWriter(vid_dir + vid_name + ' camera_speed.avi', \
    cv2.VideoWriter_fourcc(*'XVID'), cap.get(cv2.CAP_PROP_FPS), (width, height))

# initialize plot
fig, ax = plt.subplots()
line, = ax.plot([], [])
# ax.set_xlim(0, cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS))
ax.set_ylim(-2, 2)  # set appropriate ylim based on the expected range of speed
ax.set_xlabel('Time (s)')
ax.set_ylabel('Speed (ppf)')  # ppf: pixels per frame

# loop through frames
while True:
    ret, frame2 = cap.read()
    if not ret:
        break
    
    # print progress
    frame_count += 1
    #print(f'frame {frame_count}')
    
    # convert frame to grayscale
    curr_gray = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    
    # calculate optical flow using Farneback method
    flow = cv2.calcOpticalFlowFarneback(prev_gray, curr_gray, None, \
        pyr_scale, levels, winsize, iterations, poly_n, poly_sigma, flags)

    # calculate magnitude of flow vectors
    mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
    
    # calculate mean speed of camera using magnitude of flow vectors
    mean_mag = np.mean(mag)
    mean_ang = np.mean(ang)

    #if mean_ang >= 0 and mean_ang <= np.pi/2:
    #    speed = -mean_mag
    #else:
    #    speed = mean_mag
    #print(speed)
    
    speed = np.mean(mag)

    speed_list.append(speed)
    time_list.append(cap.get(cv2.CAP_PROP_POS_MSEC) / 1000)  # in seconds
    
    # update plot
    line.set_data(time_list, speed_list)
    ax.relim()
    ax.autoscale_view()
    fig.canvas.draw()
    fig_img = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8) \
        .reshape(fig.canvas.get_width_height()[::-1] + (3,))
    fig_img = cv2.cvtColor(fig_img, cv2.COLOR_RGB2BGR)
    
    # resize the plot image to match the size of the video frame
    fig_img = cv2.resize(fig_img, (frame2.shape[1], frame2.shape[0]))
    
    # add the plot image to the video frame
    frame2 = np.concatenate((frame2, fig_img), axis=1)
    
    # write output video frame
    out.write(frame2)
    
    # display the frame with the plot
    cv2.imshow('Video with Plot', frame2)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    # update previous grayscale frame
    prev_gray = curr_gray

# release video capture and writer
cap.release()
out.release()