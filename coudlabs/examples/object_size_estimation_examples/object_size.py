import wx
import os
import sys
import subprocess

class ObjectSizeEstimationApp(wx.Frame):
    def __init__(self, parent, title):
        super(ObjectSizeEstimationApp, self).__init__(parent, title=title, size=(400, 400))

        self.panel = wx.Panel(self)

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # Set the relative path to the object_size.py script
        script_path = os.path.abspath('')
        project_folder = os.path.dirname(os.path.dirname(script_path))
        model_folder = os.path.join(project_folder, 'src/object_size_estimation')
        sys.path.append(model_folder)

        # Import the map function from object_size.py
        from object_size import map

        # Create the video file section
        video_sizer = wx.BoxSizer(wx.HORIZONTAL)

        video_label = wx.StaticText(self.panel, label="Video File:")
        video_sizer.Add(video_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.video_text = wx.TextCtrl(self.panel)
        video_sizer.Add(self.video_text, 1, wx.ALL | wx.EXPAND, 5)

        video_button = wx.Button(self.panel, label="Browse")
        video_sizer.Add(video_button, 0, wx.ALL, 5)
        video_button.Bind(wx.EVT_BUTTON, self.on_browse_video)

        main_sizer.Add(video_sizer, 0, wx.EXPAND | wx.ALL, 10)

        # Create the reference label file section
        ref_sizer = wx.BoxSizer(wx.HORIZONTAL)

        ref_label = wx.StaticText(self.panel, label="Reference Object's Label File:")
        ref_sizer.Add(ref_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.ref_text = wx.TextCtrl(self.panel)
        ref_sizer.Add(self.ref_text, 1, wx.ALL | wx.EXPAND, 5)

        ref_button = wx.Button(self.panel, label="Browse")
        ref_sizer.Add(ref_button, 0, wx.ALL, 5)
        ref_button.Bind(wx.EVT_BUTTON, self.on_browse_ref)

        main_sizer.Add(ref_sizer, 0, wx.EXPAND | wx.ALL, 10)

        # Create the other label file section
        other_sizer = wx.BoxSizer(wx.HORIZONTAL)

        other_label = wx.StaticText(self.panel, label="Other Object's Label File:")
        other_sizer.Add(other_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.other_text = wx.TextCtrl(self.panel)
        other_sizer.Add(self.other_text, 1, wx.ALL | wx.EXPAND, 5)

        other_button = wx.Button(self.panel, label="Browse")
        other_sizer.Add(other_button, 0, wx.ALL, 5)
        other_button.Bind(wx.EVT_BUTTON, self.on_browse_other)

        main_sizer.Add(other_sizer, 0, wx.EXPAND | wx.ALL, 10)

        # Create the focal length section
        focal_length_sizer = wx.BoxSizer(wx.HORIZONTAL)

        focal_length_label = wx.StaticText(self.panel, label="Camera's Focal Length (pixels):")
        focal_length_sizer.Add(focal_length_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.focal_length_text = wx.TextCtrl(self.panel)
        focal_length_sizer.Add(self.focal_length_text, 1, wx.ALL | wx.EXPAND, 5)

        main_sizer.Add(focal_length_sizer, 0, wx.EXPAND | wx.ALL, 10)

        # Create the real size section
        real_size_sizer = wx.BoxSizer(wx.HORIZONTAL)

        real_size_label = wx.StaticText(self.panel, label="Reference Object Size (meters):")
        real_size_sizer.Add(real_size_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.real_size_text = wx.TextCtrl(self.panel)
        real_size_sizer.Add(self.real_size_text, 1, wx.ALL | wx.EXPAND, 5)

        main_sizer.Add(real_size_sizer, 0, wx.EXPAND | wx.ALL, 10)

        # Create the run button
        run_button = wx.Button(self.panel, label="Run Model")
        main_sizer.Add(run_button, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 10)
        run_button.Bind(wx.EVT_BUTTON, self.on_run_model)

        self.panel.SetSizer(main_sizer)
        self.Show()

    def on_browse_video(self, event):
        wildcard = "Video Files (*.mp4)|*.mp4"
        dialog = wx.FileDialog(self, "Select Video File", wildcard=wildcard, style=wx.FD_OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            path = dialog.GetPath()
            self.video_text.SetValue(path)
        dialog.Destroy()

    def on_browse_ref(self, event):
        dialog = wx.FileDialog(self, "Select Reference Object's Label File", style=wx.FD_OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            path = dialog.GetPath()
            self.ref_text.SetValue(path)
        dialog.Destroy()

    def on_browse_other(self, event):
        dialog = wx.FileDialog(self, "Select Other Object's Label File", style=wx.FD_OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            path = dialog.GetPath()
            self.other_text.SetValue(path)
        dialog.Destroy()

    def on_run_model(self, event):
        video_path = self.video_text.GetValue()
        file_path_ref = self.ref_text.GetValue()
        file_path_other = self.other_text.GetValue()
        focal_length = float(self.focal_length_text.GetValue())
        real_size_ref = float(self.real_size_text.GetValue())

        if not os.path.isfile(video_path):
            wx.MessageBox("Invalid video file", "Error", wx.OK | wx.ICON_ERROR)
            return

        if not os.path.isfile(file_path_ref):
            wx.MessageBox("Invalid reference file", "Error", wx.OK | wx.ICON_ERROR)
            return

        if not os.path.isfile(file_path_other):
            wx.MessageBox("Invalid other file", "Error", wx.OK | wx.ICON_ERROR)
            return

        try:
            subprocess.call(["python", "object_size.py", video_path, file_path_ref, file_path_other, str(real_size_ref), str(focal_length)])
        except Exception as e:
            wx.MessageBox(str(e), "Error", wx.OK | wx.ICON_ERROR)

if __name__ == '__main__':
    app = wx.App()
    ObjectSizeEstimationApp(None, "Object Size Estimation")
    app.MainLoop()
