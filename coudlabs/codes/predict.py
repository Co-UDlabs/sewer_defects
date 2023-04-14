from ultralytics import YOLO
from ultralytics.yolo.engine.results import Boxes
import cv2
import os

# best model and data paths
bestModelPath = "C:\\Ehsan\\sewer_defects\\coudlabs\\runs\\detect\\train2\\weights\\best.pt"
imageFolder = "C:\\Ehsan\\sewer_defects\\coudlabs\\prediction\\coudlabs01\\"

# load model
bestModel = YOLO(bestModelPath)

# loop on images & videos in imageFolder
for filename in os.listdir(imageFolder):
    img = imageFolder+filename
    if img is not None:
        # get result
        result = bestModel(img, save=True)
        # get size of bounding box
        # to get all box information use "box = result[0].boxes.numpy()""   
        # for properties see ..\ultralytics\yolo\engine\results.py lines 170 to 178
        # size of bounding box relative to image size
        xyxyn = result[0].boxes.numpy().xyxyn

