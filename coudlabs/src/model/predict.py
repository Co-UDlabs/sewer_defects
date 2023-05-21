from ultralytics import YOLO
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
