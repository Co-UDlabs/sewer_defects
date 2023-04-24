import os
import random
import shutil

# Set the percentages for each subset (should add up to 100)
subset1_percent = 70
subset2_percent = 15
subset3_percent = 15

# Set the paths for the source folder and the three destination folders
source_images = 'C:/Ehsan/sewer_data/images/'
source_labels = 'C:/Ehsan/sewer_data/labels/'

# Set the local paths for the three folders where the downloaded files will be saved
destination_dir = "C:/Ehsan/sewer_defects/coudlabs/data/test_01"
train_images = destination_dir + "/images/training/"
train_labels = destination_dir + "/labels/training/"
valid_images = destination_dir + "/images/validation/"
valid_labels = destination_dir + "/labels/validation/"
test_images = destination_dir + "/images/test/"
test_labels = destination_dir + "/labels/test/"

# Destination folders (to be overwritten))
for folder in [train_images,valid_images,test_images,train_labels,valid_labels,test_labels]:
    if os.path.exists(folder):
        os.remove(folder)
    os.makedirs(folder)

# Get the list of files in the source folder
file_list = os.listdir(source_images)

# Calculate the number of files for each subset based on the percentages
nsub1 = int(len(file_list) * subset1_percent / 100)
nsub2 = int(len(file_list) * subset2_percent / 100)
nsub3 = int(len(file_list) * subset3_percent / 100)

# Shuffle the list of files
random.shuffle(file_list)

# 
files_subset1 = file_list[0:nsub1]
files_subset2 = file_list[nsub1:nsub1+nsub2]
files_subset3 = file_list[nsub1+nsub2:nsub1+nsub2+nsub3]

# Copy images to the destination folders based on the subset percentages
for i, file in enumerate(files_subset1):
    shutil.copy(os.path.join(source_images, file), train_images)
for i, file in enumerate(files_subset2):
    shutil.copy(os.path.join(source_images, file), valid_images)
for i, file in enumerate(files_subset3):
    shutil.copy(os.path.join(source_images, file), test_images)

# Copy labels
l = [os.path.splitext(x)[0] for x in files_subset1]
l = [x + '.txt' for x in l]
for i, file in enumerate(l):
    shutil.copy(os.path.join(source_labels, file), train_labels)
l = [os.path.splitext(x)[0] for x in files_subset2]
l = [x + '.txt' for x in l]
for i, file in enumerate(l):
    shutil.copy(os.path.join(source_labels, file), valid_labels)
l = [os.path.splitext(x)[0] for x in files_subset3]
l = [x + '.txt' for x in l]
for i, file in enumerate(l):
    shutil.copy(os.path.join(source_labels, file), test_labels)