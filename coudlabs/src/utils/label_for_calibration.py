import os
import glob
import csv

# Data
input_path = "C:/Users/ci1ek/Desktop/Motion/calib_pipe"
file_paths = glob.glob(os.path.join(input_path, '*.txt'))

# Lists to store the output
data_list = []

# Loop on the text files
for file_path in file_paths:
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line:  # Ignore empty lines
                data = line.split()  # Split the line into columns

                # Extract the relevant information
                x0 = float(data[1])
                y0 = float(data[2])
                width = float(data[3])
                height = float(data[4])

                # Add to the list
                data_list.append([x0, y0, width, height])

# Save output
output_file_path = os.path.join(input_path,"box_orient.csv")
with open(output_file_path, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data_list)

print("Done!")