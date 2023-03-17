
# pip install --upgrade ultralytics
# pip install -r C:\Ehsan\sewer_defects\ultralytics\requirements.txt

import ultralytics
ultralytics.checks()
from ultralytics import YOLO

# data
dataPath = "C:\\Ehsan\\sewer_defects\\coudlabs\\data\\coudlab_example.yaml"

# load a model
# model = YOLO("yolov8n.yaml")  # build a new model from scratch
model = YOLO("yolov8n.pt")  # load a pretrained model (recommended for training)

# train model
model.train(data=dataPath, epochs=100, imgsz=352)

# evaluate model performance on the validation set
val_metrics = model.val() 

# export model
success = model.export(format="onnx")  # export the model to ONNX format