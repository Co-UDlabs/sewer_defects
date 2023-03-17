from ultralytics import YOLO
import cv2
import os

# best model and data paths
bestModelPath = "C:\\Ehsan\\sewer_defects\\coudlabs\\runs\\detect\\train2\\weights\\best.pt"
imageFolder = "C:\\Ehsan\\sewer_defects\\coudlabs\\prediction\\coudlabs01\\"

# load model
bestModel = YOLO(bestModelPath)

# loop on images
for filename in os.listdir(imageFolder):
    img = cv2.imread(os.path.join(imageFolder,filename))
    if img is not None:
        # get result
        result = bestModel(img)  # predict on an image
        #print(result[0])
        # plot result
        resImg = result[0].plot()
        cv2.imshow("result", resImg)
        cv2.waitKey(1)
        # write result
        fname, fext = os.path.splitext(filename)
        cv2.imwrite(imageFolder+fname+'_out'+fext,resImg)