
# pip install --upgrade ultralytics
# pip install -r C:\Ehsan\sewer_defects\ultralytics\requirements.txt

import ultralytics
ultralytics.checks()
from ultralytics import YOLO
from tvp import train, validate

# data
trainingDataPath = "C:\\Ehsan\\sewer_defects\\ultralytics\\ultralytics\\datasets\\coudlab_example.yaml"

# load a model
# model = YOLO("yolov8n.yaml")  # build a new model from scratch
model = YOLO("yolov8n.pt")  # load a pretrained model (recommended for training)

# train model
model.train(data=trainingDataPath, epochs=30, imgsz=352)

# evaluate model performance on the validation set
metrics = model.val()  # evaluate model performance on the validation set

# export model
success = model.export(format="onnx")  # export the model to ONNX format

