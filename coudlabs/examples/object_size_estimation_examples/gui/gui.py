import os
import sys
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

# Set the relative path to the object_size.py script
script_path = os.path.abspath('')
project_folder = os.path.dirname(os.path.dirname(script_path))
model_folder = os.path.join(project_folder, 'src/object_size_estimation')
sys.path.append(model_folder)

# Import the map function from object_size.py
from object_size import map

def select_video_file():
    video_file = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4")])
    video_entry.delete(0, tk.END)
    video_entry.insert(tk.END, video_file)

def select_reference_file():
    ref_file = filedialog.askopenfilename()
    ref_entry.delete(0, tk.END)
    ref_entry.insert(tk.END, ref_file)

def select_other_file():
    other_file = filedialog.askopenfilename()
    other_entry.delete(0, tk.END)
    other_entry.insert(tk.END, other_file)

def run_object_size_estimation():
    # Get the input values
    video_path = video_entry.get()
    file_path_ref = ref_entry.get()
    file_path_other = other_entry.get()
    focal_length = float(focal_length_entry.get())
    real_size_ref = float(real_size_entry.get())
    
    # Validate the input values
    if not os.path.isfile(video_path):
        messagebox.showerror("Error", "Invalid video file")
        return
    if not os.path.isfile(file_path_ref):
        messagebox.showerror("Error", "Invalid reference file")
        return
    if not os.path.isfile(file_path_other):
        messagebox.showerror("Error", "Invalid other file")
        return
    
    # Run the model
    try:
        map(video_path, file_path_ref, file_path_other, real_size_ref, focal_length)
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Create the main window
window = tk.Tk()
window.title("Object Size Estimation")

# Video File
select_video_button = tk.Button(window, text="Select Video File", command=select_video_file)
select_video_button.grid(row=0, column=0, padx=10, pady=10, sticky="w")
video_entry = tk.Entry(window, width=40)
video_entry.grid(row=0, column=1, padx=10, pady=10, sticky="e")

# Reference Label File
select_ref_button = tk.Button(window, text="Select Reference Object's Label File", command=select_reference_file)
select_ref_button.grid(row=1, column=0, padx=10, pady=10, sticky="w")
ref_entry = tk.Entry(window, width=40)
ref_entry.grid(row=1, column=1, padx=10, pady=10, sticky="e")

# Other Label File
select_other_button = tk.Button(window, text="Select Other Object's Label File", command=select_other_file)
select_other_button.grid(row=2, column=0, padx=10, pady=10, sticky="w")
other_entry = tk.Entry(window, width=40)
other_entry.grid(row=2, column=1, padx=10, pady=10, sticky="e")

# Focal Length
focal_length_label = tk.Label(window, text="Camera's Focal Length (pixels):")
focal_length_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")
focal_length_entry = tk.Entry(window, width=40)
focal_length_entry.grid(row=3, column=1, padx=10, pady=10, sticky="e")

# Object Size
real_size_label = tk.Label(window, text="Reference Object Size (meters):")
real_size_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")
real_size_entry = tk.Entry(window, width=40)
real_size_entry.grid(row=4, column=1, padx=10, pady=10, sticky="e")

# Run Model Button
run_button = tk.Button(window, text="Run Model", command=run_object_size_estimation)
run_button.grid(row=5, column=0, columnspan=2, pady=10)

# Adjust the window size to fit all elements
window.update()
window_width = window.winfo_reqwidth()
window_height = window.winfo_reqheight()
window.geometry(f"{window_width}x{window_height}")

# Start the main loop
window.mainloop()