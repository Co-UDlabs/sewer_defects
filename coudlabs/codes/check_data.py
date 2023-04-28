import cv2
import os
import glob
import pandas as pd
import shutil
from PIL import ImageColor

# Data directory
data_dir = "C:\Ehsan\sewer_data"

# Image file extensions
extensions = ["png", "jpg", "tif", "bmp"]

# Label names
text_file = open(os.path.join(data_dir,"label_names.txt"), "r")
label_ids = text_file.read().split('\n')
print("Label IDs:")
print(label_ids)

# Label colours
color_names = ["red", "chartreuse", "forestgreen", "steelblue", \
    "gold", "aqua", "orchid", "purple", "firebrick"]
label_colors = []
for color in color_names:
    label_colors.append(ImageColor.getrgb(color))

# plot specs
line_thickness = 3
font = cv2.FONT_HERSHEY_DUPLEX
font_scale = 1.75
font_thickness = 3

# Paths
image_path = data_dir + "/labelled images"
write_path = data_dir + "/show labels"
if os.path.exists(write_path):
    shutil.rmtree(write_path)
os.makedirs(write_path)

# List of image files in the folder
image_list = []
for ext in extensions:
    image_list.extend(glob.glob(os.path.join(image_path, f'*.{ext}')))

# write list of files in a text file
listname = os.path.join(data_dir,'file_list.csv')
with open(listname, mode="w") as outfile:  # also, tried mode="rb"
    for s in image_list:
        outfile.write("%s\n" % s)

# Label file column names
colnames = ["label", "xc", "yc", "w", "h"]

# Iterate over files
for file in image_list:
    # folder path, file name and file extension
    folder, file_name_with_extension = os.path.split(file)
    file_name, file_extension = os.path.splitext(file_name_with_extension)
    # print file name
    print("\n" + file_name + file_extension + ":")
    # load the image
    img = cv2.imread(file)
    # Get the image's height and width
    height, width = img.shape[:2]
    # label file
    label_file = os.path.join(folder, file_name + ".txt")
    # read labels from file
    labels = pd.read_csv(label_file, sep=" ", names=colnames)
    # make sure indices pair with number of rows
    labels = labels.reset_index()
    # if there is at least one label:
    if not labels.empty:
        # print file contents
        print(labels)
        # read each label
        for i, row in labels.iterrows():
            # label number
            lid = int(row.label)
            # bounding box coordinates of rectangle's four vertices (relative to image width and height)
            vertices = [(row['xc']+row['w']/2, row['yc']+row['h']/2), \
                        (row['xc']+row['w']/2, row['yc']-row['h']/2), \
                        (row['xc']-row['w']/2, row['yc']-row['h']/2), \
                        (row['xc']-row['w']/2, row['yc']+row['h']/2)]
            # Convert vertex coordinates from relative to absolute pixel values
            abs_vertices = [(int(vertex[0] * width), int(vertex[1] * height)) for vertex in vertices]
            # draw rectangle on image
            cv2.rectangle(img, abs_vertices[0], abs_vertices[2], label_colors[lid], line_thickness)
            # get width and height of text box
            (text_width, text_height) = cv2.getTextSize(label_ids[lid], \
                font, fontScale=font_scale, thickness=font_thickness)[0]
            # position of text box
            text_offset_x = abs_vertices[2][0]
            text_offset_y = abs_vertices[2][1]
            # draw white rectangle for text
            cv2.rectangle(img, (text_offset_x, text_offset_y), (text_offset_x + \
                text_width, text_offset_y + text_height), label_colors[lid], cv2.FILLED)
            # add text to image
            cv2.putText(img, label_ids[lid], (text_offset_x, text_offset_y + text_height), \
                font, font_scale, (255, 255, 255), font_thickness, cv2.LINE_AA)
    # Save image
    cv2.imwrite(os.path.join(write_path, file_name + " checked" + file_extension), img)
