'''
File name: change_labels.py
Author: Ehsan Kazemi
Date created: Apr 2023
Date last modified: 28 Apr 2023
-------------------------------------------------------------------------\
 This code searches through all the text files in the image data folder, /
 replaces the existing label numbers (present in the first column in the \
 label text files) with the new numbers that associate with the new      /
 label names, and writes the updated data to the text files.             \
 Be careful! This code overwrites the existing text files. If you run it /
 you will cjange the label numbers permanemtly. Therefore, make sure a   \
 copy of the label text files is backed up already.                      /
-------------------------------------------------------------------------\
'''

# Import dependencies
import os

# Define the folder path and the numbers to replace
folder_path = "C:\Ehsan\sewer_data\labelled images"
old_numbers = [1, 5, 6, 7, 8]
new_numbers = [0, 4, 5, 6, 7]

# Loop through all files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".txt"):  # Only process text files
        # Read the data from the input file
        with open(os.path.join(folder_path, filename), "r") as input_file:
            data = input_file.readlines()
        
        # Update the data
        for i in range(len(data)):
            row = data[i].split()  # Split the row by whitespace
            try:
                # Check if the first column is in the list of numbers to replace
                if int(row[0]) in old_numbers:
                    # Replace the first column with the corresponding new number
                    row[0] = str(new_numbers[old_numbers.index(int(row[0]))])
                    data[i] = " ".join(row) + "\n"  # Join the row and add a newline
            except ValueError:
                # Ignore any rows that can't be converted to an integer in the first column
                pass
        
        # Write the updated data to the output file
        with open(os.path.join(folder_path, filename), "w") as output_file:
            output_file.writelines(data)