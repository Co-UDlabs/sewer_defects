import os
import glob
import random
import shutil
from PIL import Image

# name of dataset
data_name = "d1"

# Set the paths for the source folder and the three destination folders
source_path = 'C:/Ehsan/sewer_data/labelled images'

# file extensions
extensions = ["png", "jpg", "tif", "bmp"]

# convert to grey? "y" or "n"
cl2gry = "y"

# Set the percentages for each subset (should add up to 100)
subset1_percent = 70
subset2_percent = 15
subset3_percent = 15

# Set the local paths for the three folders where the downloaded files will be saved
destination_dir = "C:/Ehsan/sewer_defects/coudlabs/data/" + data_name
train_images = destination_dir + "/images/training/"
train_labels = destination_dir + "/labels/training/"
valid_images = destination_dir + "/images/validation/"
valid_labels = destination_dir + "/labels/validation/"
test_images = destination_dir + "/images/test/"
test_labels = destination_dir + "/labels/test/"

# Destination folders (to be overwritten))
for folder in [train_images,valid_images,test_images,train_labels,valid_labels,test_labels]:
    if os.path.exists(folder):
        shutil.rmtree(folder)
    os.makedirs(folder)

# List of image files in source path
image_list = []
for ext in extensions:
    image_list.extend(glob.glob(os.path.join(source_path, f'*.{ext}')))

# Calculate the number of files for each subset based on the percentages
nsub1 = int(len(image_list) * subset1_percent / 100)
nsub2 = int(len(image_list) * subset2_percent / 100)
nsub3 = int(len(image_list) * subset3_percent / 100)

# Splid images intwo three subsets (training / validation / test) randomly
random.shuffle(image_list)
files_subset1 = image_list[0:nsub1]
files_subset2 = image_list[nsub1:nsub1+nsub2]
files_subset3 = image_list[nsub1+nsub2:nsub1+nsub2+nsub3]

# Function to convert images into grey and then 
# copy images and labels to the destination folders
def process_file(image_path,image_destination,label_destination):
    missing_label_files = []
    for file in image_path:
        # folder path, file name and file extension
        folder, file_name_with_extension = os.path.split(file)
        file_name, file_extension = os.path.splitext(file_name_with_extension)
        # convert image to grey?
        if cl2gry == 'y':  # convert
            image = Image.open(file)
            image = image.convert('L')
            image.save(os.path.join(image_destination, file_name + file_extension))
        else:   # just copy the original image
            shutil.copy(file, image_destination)
        # label file
        label_file = os.path.join(folder, file_name + ".txt")
        if os.path.isfile(label_file):
            shutil.copy(label_file, label_destination)
        else:
            missing_label_files.append(label_file)
    if missing_label_files:
        raise Exception("ERROR: the following label files are missing: ", missing_label_files)

# Copy files
process_file(files_subset1,train_images,train_labels)
process_file(files_subset2,valid_images,valid_labels)
process_file(files_subset3,test_images,test_labels)