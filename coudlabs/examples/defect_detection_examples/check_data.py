'''
File name: check_data_gui.py
Author: Ehsan Kazemi
Date created: Jun 2023
Date last modified: 08/06/2023

-------------------------------------------------------------------------\
This code creates a GUI window with a text field for the data directory, /
a "Browse" button to select the directory, image file extension buttons  \
arranged in a 3x3 grid, and a "Process Data" button. The selected data   /
directory and image file extensions are used to process the images and   \
save the labeled images in the "show_labels" folder. Note: The code      /
assumes that you have the necessary dependencies (OpenCV, pandas)        \
installed and accessible in your environment.                            /
-------------------------------------------------------------------------\
'''

import wx
import os
import cv2
import glob
import pandas as pd
import shutil

class ImageProcessingApp(wx.Frame):
    def __init__(self, parent, title):
        super(ImageProcessingApp, self).__init__(parent, title=title)

        # Set the panel
        self.panel = wx.Panel(self)

        # Create the main sizer
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # Create the input path section
        input_path_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Input path label
        input_path_label = wx.StaticText(self.panel, label="Input Path:")
        input_path_sizer.Add(input_path_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        # Input path text control
        self.input_path_text = wx.TextCtrl(self.panel)
        input_path_sizer.Add(self.input_path_text, 1, wx.EXPAND | wx.ALL, 5)

        # Input path browse button
        browse_button = wx.Button(self.panel, label="Browse")
        input_path_sizer.Add(browse_button, 0, wx.ALL, 5)
        browse_button.Bind(wx.EVT_BUTTON, self.on_browse)

        # Add the input path section to the main sizer
        main_sizer.Add(input_path_sizer, 0, wx.EXPAND | wx.ALL, 10)

        # Create the file extensions section
        extensions_sizer = wx.GridSizer(3, 3, 5, 5)

        # Image file extensions
        image_extensions = [".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff", ".ico", ".webp", ".svg"]

        # Create buttons for each extension
        self.extension_buttons = []
        for ext in image_extensions:
            button = wx.ToggleButton(self.panel, label=ext)
            extensions_sizer.Add(button, 0, wx.EXPAND)
            self.extension_buttons.append(button)

        # Add the file extensions section to the main sizer
        main_sizer.Add(extensions_sizer, 0, wx.EXPAND | wx.ALL, 10)

        # Create the process data button
        process_button = wx.Button(self.panel, label="Process Data")
        main_sizer.Add(process_button, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        process_button.Bind(wx.EVT_BUTTON, self.process_data)

        # Set the main sizer
        self.panel.SetSizer(main_sizer)

        # Set the window size
        self.SetSize(400, 300)

        # Show the frame
        self.Show()

    def on_browse(self, event):
        dialog = wx.DirDialog(self.panel, message="Select the input path", style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
        if dialog.ShowModal() == wx.ID_OK:
            path = dialog.GetPath()
            self.input_path_text.SetValue(path)
        dialog.Destroy()

    def process_data(self, event):
        # Get the input path
        data_dir = self.input_path_text.GetValue()

        # Get the selected file extensions
        extensions = [button.GetLabel() for button in self.extension_buttons if button.GetValue()]

        # Perform image processing
        self.process_images(data_dir, extensions)

    def process_images(self, data_dir, extensions):
        # Dictionary mapping color names to RGB values
        color_dict = {'red': (255, 0, 0), 'green': (0, 255, 0), 'blue': (0, 0, 255), 'turquoiseblue': (0, 199, 140),
                      'banana': (227, 207, 87), 'yellow2': (238, 238, 0), 'violetred1': (255, 62, 150),
                      'violetred3': (205, 50, 120), 'violetred4': (139, 34, 82), 'blue2': (0, 0, 238),
                      'springgreen3': (0, 139, 69), 'brown1': (255, 64, 64), 'brown4': (139, 35, 35),
                      'burlywood1': (255, 211, 155), 'sapgreen': (48, 128, 20), 'deepskyblue1': (0, 191, 255)}

        # Label names
        text_file = open(os.path.join(data_dir, "label_names.txt"), "r")
        label_ids = text_file.read().split('\n')
        print("Label IDs:")
        print(label_ids)

        # Label colours
        color_names = ["green", "turquoiseblue", "springgreen3",
                       "banana", "deepskyblue1", "violetred1", "violetred3", "brown1"]
        label_colors = []
        for color in color_names:
            label_colors.append(color_dict.get(color.lower()))

        # plot specs
        line_thickness = 3
        font = cv2.FONT_HERSHEY_DUPLEX
        font_scale = 1
        font_thickness = 2

        # Paths
        image_path = os.path.join(data_dir, "labelled_images")
        write_path = os.path.join(data_dir, "show_labels")
        if os.path.exists(write_path):
            shutil.rmtree(write_path)
        os.makedirs(write_path)

        print("Read from", image_path)

        # List of image files in the folder
        image_list = []
        for ext in extensions:
            image_list.extend(glob.glob(os.path.join(image_path, f'*{ext}')))

        # Write list of files into a file
        listname = os.path.join(data_dir, 'file_list.csv')
        with open(listname, mode="w") as outfile:
            for s in sorted(image_list):
                outfile.write("%s\n" % s)

        # Label file column names
        colnames = ["label", "xc", "yc", "w", "h"]

        # Iterate over files
        for file in image_list:
            # Folder path, file name, and file extension
            folder, file_name_with_extension = os.path.split(file)
            file_name, file_extension = os.path.splitext(file_name_with_extension)

            # Load the image
            img = cv2.imread(file)

            # Get the image's height and width
            height, width = img.shape[:2]

            # Label file
            label_file = os.path.join(folder, file_name + ".txt")

            # Read labels from file
            labels = pd.read_csv(label_file, sep=" ", names=colnames)

            # Make sure indices pair with the number of rows
            labels = labels.reset_index()

            # Print number, file name, and number of labels (or "No labels" if there are none)
            label_count = len(labels.index)
            label_str = f"{label_count} {'label' if label_count == 1 else 'labels'}" if label_count > 0 else "No labels"
            print(f"{image_list.index(file) + 1}, {file_name + file_extension}, {label_str}")

            # Iterate over labels
            for _, label in labels.iterrows():
                # Label ID
                label_id = int(label["label"])

                # Object class label
                label_name = label_ids[label_id]

                # Object bounding box coordinates
                x_center = int(label["xc"] * width)
                y_center = int(label["yc"] * height)
                box_width = int(label["w"] * width)
                box_height = int(label["h"] * height)

                # Bounding box top-left corner coordinates
                x_top_left = int(x_center - box_width / 2)
                y_top_left = int(y_center - box_height / 2)

                # Bounding box bottom-right corner coordinates
                x_bottom_right = int(x_center + box_width / 2)
                y_bottom_right = int(y_center + box_height / 2)

                # Draw the bounding box and label text on the image
                cv2.rectangle(img, (x_top_left, y_top_left), (x_bottom_right, y_bottom_right), label_colors[label_id],
                              line_thickness)
                cv2.putText(img, label_name, (x_top_left, y_top_left - 10), font, font_scale, label_colors[label_id],
                            font_thickness)

            # Save the image with bounding boxes and labels
            write_name = os.path.join(write_path, file_name + ".png")
            cv2.imwrite(write_name, img)

        print("Finished processing images.")

        # Show a message box indicating the process is complete
        wx.MessageBox("Image processing is complete!", "Info", wx.OK | wx.ICON_INFORMATION)


if __name__ == "__main__":
    app = wx.App()
    frame = ImageProcessingApp(None, title="Image Processing App")
    app.MainLoop()