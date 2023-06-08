from ultralytics import YOLO
import os
import datetime

def predict(data_path, model_path):
    
    # load model
    bestModel = YOLO(model_path)

    # Generate path name to save output
    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    subfolder_name = f"predicted_{current_datetime}"
    
    # loop on images & videos in imageFolder
    for filename in os.listdir(data_path):
        img = os.path.join(data_path,filename)
        if img is not None:
            # get result
            result = bestModel(img, save=True, project=data_path, name=subfolder_name)