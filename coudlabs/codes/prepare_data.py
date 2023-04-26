import os
import glob
import random
import shutil

# name of dataset
data_name = "data_01"

# Set the paths for the source folder and the three destination folders
source_path = 'C:/Ehsan/sewer_data/labelled images'

# file extensions
extensions = ["png", "jpg", "tif", "bmp"]

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

# File names
file_names = [os.path.splitext(file)[0] for file in image_list]

# Calculate the number of files for each subset based on the percentages
nsub1 = int(len(image_list) * subset1_percent / 100)
nsub2 = int(len(image_list) * subset2_percent / 100)
nsub3 = int(len(image_list) * subset3_percent / 100)

# Splid images intwo three subsets (training / validation / test) randomly
random.shuffle(image_list)
files_subset1 = image_list[0:nsub1]
files_subset2 = image_list[nsub1:nsub1+nsub2]
files_subset3 = image_list[nsub1+nsub2:nsub1+nsub2+nsub3]

# Function to copy images and labels to the destination folders
def copy_files(image_files,image_folder,label_folder):
    missing_text_files = []
    for file in image_files:
        shutil.copy(os.path.join(source_path, file), image_folder)
        text_file = os.path.splitext(file)[0] + ".txt"
        if os.path.isfile(os.path.join(source_path, text_file)):
            shutil.copy(os.path.join(source_path, text_file), label_folder)
        else:
            missing_text_files.append(text_file)
    if missing_text_files:
        raise Exception("ERROR: the following label files are missing: ", missing_text_files)

# Copy files
copy_files(files_subset1,train_images,train_labels)
copy_files(files_subset2,valid_images,valid_labels)
copy_files(files_subset3,test_images,test_labels)
