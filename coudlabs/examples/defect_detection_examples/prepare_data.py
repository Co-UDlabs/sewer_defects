import wx
import os
import glob
import random
import cv2
import shutil
import re

class DataProcessingApp(wx.Frame):
    def __init__(self, parent, title):
        super(DataProcessingApp, self).__init__(parent, title=title, size=(400, 400))

        self.panel = wx.Panel(self)

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # Create the data name section
        data_name_sizer = wx.BoxSizer(wx.HORIZONTAL)

        data_name_label = wx.StaticText(self.panel, label="Data Name:")
        data_name_sizer.Add(data_name_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.data_name_text = wx.TextCtrl(self.panel)
        data_name_sizer.Add(self.data_name_text, 1, wx.ALL | wx.EXPAND, 5)

        main_sizer.Add(data_name_sizer, 0, wx.EXPAND | wx.ALL, 10)

        # Create the labelled images path section
        labelled_images_sizer = wx.BoxSizer(wx.HORIZONTAL)

        labelled_images_label = wx.StaticText(self.panel, label="Labelled Images Path:")
        labelled_images_sizer.Add(labelled_images_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.labelled_images_path_text = wx.TextCtrl(self.panel)
        labelled_images_sizer.Add(self.labelled_images_path_text, 1, wx.ALL | wx.EXPAND, 5)

        labelled_images_button = wx.Button(self.panel, label="Browse")
        labelled_images_sizer.Add(labelled_images_button, 0, wx.ALL, 5)
        labelled_images_button.Bind(wx.EVT_BUTTON, self.on_browse)

        main_sizer.Add(labelled_images_sizer, 0, wx.EXPAND | wx.ALL, 10)

        # Create the destination directory section
        destination_dir_sizer = wx.BoxSizer(wx.HORIZONTAL)

        destination_dir_label = wx.StaticText(self.panel, label="Destination Directory:")
        destination_dir_sizer.Add(destination_dir_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.destination_dir_text = wx.TextCtrl(self.panel)
        destination_dir_sizer.Add(self.destination_dir_text, 1, wx.ALL | wx.EXPAND, 5)

        destination_dir_button = wx.Button(self.panel, label="Browse")
        destination_dir_sizer.Add(destination_dir_button, 0, wx.ALL, 5)
        destination_dir_button.Bind(wx.EVT_BUTTON, self.on_browse_destination_dir)

        main_sizer.Add(destination_dir_sizer, 0, wx.EXPAND | wx.ALL, 10)

        # Create the grayscale conversion checkbox
        self.convert_checkbox = wx.CheckBox(self.panel, label="Convert to Grayscale")
        main_sizer.Add(self.convert_checkbox, 0, wx.ALL, 10)

        # Create the percentages section
        percentages_sizer = wx.GridSizer(3, 2, 5, 5)

        train_label = wx.StaticText(self.panel, label="Train Percentage:")
        percentages_sizer.Add(train_label, 0, wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 5)
        self.train_text = wx.TextCtrl(self.panel)
        percentages_sizer.Add(self.train_text, 0, wx.ALL | wx.EXPAND, 5)

        valid_label = wx.StaticText(self.panel, label="Valid Percentage:")
        percentages_sizer.Add(valid_label, 0, wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 5)
        self.valid_text = wx.TextCtrl(self.panel)
        percentages_sizer.Add(self.valid_text, 0, wx.ALL | wx.EXPAND, 5)

        test_label = wx.StaticText(self.panel, label="Test Percentage:")
        percentages_sizer.Add(test_label, 0, wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 5)
        self.test_text = wx.TextCtrl(self.panel)
        percentages_sizer.Add(self.test_text, 0, wx.ALL | wx.EXPAND, 5)

        main_sizer.Add(percentages_sizer, 0, wx.EXPAND | wx.ALL, 10)

        # Create the process button
        process_button = wx.Button(self.panel, label="Process Data")
        process_button.Bind(wx.EVT_BUTTON, self.on_process)
        main_sizer.Add(process_button, 0, wx.ALL | wx.ALIGN_CENTER, 10)

        self.panel.SetSizer(main_sizer)
        self.Show()

    def on_browse(self, event):
        dlg = wx.DirDialog(self, "Choose Labelled Images Path")
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.labelled_images_path_text.SetValue(path)
        dlg.Destroy()

    def on_browse_destination_dir(self, event):
        dlg = wx.DirDialog(self, "Choose Destination Directory")
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.destination_dir_text.SetValue(path)
        dlg.Destroy()

    def on_process(self, event):
        # Get the input values
        data_name = self.data_name_text.GetValue()
        labelled_images_path = self.labelled_images_path_text.GetValue()
        destination_dir = self.destination_dir_text.GetValue()
        convert_to_grayscale = self.convert_checkbox.GetValue()
        train_percentage = int(self.train_text.GetValue())
        valid_percentage = int(self.valid_text.GetValue())
        test_percentage = int(self.test_text.GetValue())

        # Validate the input values
        if not data_name:
            wx.MessageBox("Please enter a data name.", "Error", wx.OK | wx.ICON_ERROR)
            return

        if not labelled_images_path:
            wx.MessageBox("Please select the labelled images path.", "Error", wx.OK | wx.ICON_ERROR)
            return

        if not destination_dir:
            wx.MessageBox("Please select the destination directory.", "Error", wx.OK | wx.ICON_ERROR)
            return

        # Create the output directories
        output_dir = os.path.join(destination_dir, data_name)
        image_dir = os.path.join(output_dir, "images")
        labels_dir = os.path.join(output_dir, "labels")
        train_dir = os.path.join(image_dir, "train")
        valid_dir = os.path.join(image_dir, "validation")
        test_dir = os.path.join(image_dir, "test")
        train_labels_dir = os.path.join(labels_dir, "training")
        valid_labels_dir = os.path.join(labels_dir, "validation")
        test_labels_dir = os.path.join(labels_dir, "test")
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(image_dir, exist_ok=True)
        os.makedirs(labels_dir, exist_ok=True)
        os.makedirs(train_dir, exist_ok=True)
        os.makedirs(valid_dir, exist_ok=True)
        os.makedirs(test_dir, exist_ok=True)
        os.makedirs(train_labels_dir, exist_ok=True)
        os.makedirs(valid_labels_dir, exist_ok=True)
        os.makedirs(test_labels_dir, exist_ok=True)

        # Get the list of image files in the labelled images path
        image_files = sum((glob.glob(os.path.join(labelled_images_path, ext)) for ext in \
            ['*.jpeg', '*.jpg', '*.bmp', '*.png', '*.tiff', '*.gif', '*.ico', '*.webp', '*.svg']), [])

        # Shuffle the image files list
        random.shuffle(image_files)

        # Calculate the number of images for each set
        num_images = len(image_files)
        num_train = int(num_images * train_percentage / 100)
        num_valid = int(num_images * valid_percentage / 100)
        num_test = int(num_images * test_percentage / 100)

        # Split the image files into train, validation, and test sets
        train_files = image_files[:num_train]
        valid_files = image_files[num_train : num_train + num_valid]
        test_files = image_files[num_train + num_valid : num_train + num_valid + num_test]

        # Copy the images and labels to the respective directories
        print(f'Training data set ... {train_percentage}% of data')
        self.copy_files(train_files, train_dir, train_labels_dir)
        print(f'Validation data set ... {valid_percentage}% of data')
        self.copy_files(valid_files, valid_dir, valid_labels_dir)
        print(f'Test data set ... {test_percentage}% of data')
        self.copy_files(test_files, test_dir, test_labels_dir)

        # Convert images to grayscale if selected
        if convert_to_grayscale:
            self.convert_to_grayscale(train_dir)
            self.convert_to_grayscale(valid_dir)
            self.convert_to_grayscale(test_dir)

        wx.MessageBox("Data processing completed.", "Success", wx.OK | wx.ICON_INFORMATION)

    def copy_files(self, files, image_dir, labels_dir):
        for file in files:
            # Copy image file
            shutil.copy(file, image_dir)

            # Copy corresponding label file
            label_file = re.sub(r"\.(?:jpg|jpeg|bmp|png|tiff|gif|ico|webp|svg)$", ".txt", file, flags=re.IGNORECASE)
            if os.path.exists(label_file):
                shutil.copy(label_file, labels_dir)

    def convert_to_grayscale(self, image_dir):
        image_extensions = ['*.jpg', '*.jpeg', '*.bmp', '*.png', '*.tiff', '*.gif', '*.ico', '*.webp', '*.svg']
        images = []
        for extension in image_extensions:
            images.extend(glob.glob(os.path.join(image_dir, extension)))

        for image_file in images:
            image = cv2.imread(image_file)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            cv2.imwrite(image_file, gray)

app = wx.App()
DataProcessingApp(None, title="Data Processing App")
app.MainLoop()