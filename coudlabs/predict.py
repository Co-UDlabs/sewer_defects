from ultralytics import YOLO
import cv2

# best model and data paths
bestModelPath = "C:\Ehsan\\sewer_defects\\coudlabs\\runs\\detect\\train\\weights\\best.pt"
imagePath = "C:\\Ehsan\\sewer_defects\\coudlabs\\prediction\\01\\obstacle_test.jpg"

# load model
bestModel = YOLO(bestModelPath)

# get result
img = cv2.imread(imagePath)
result = bestModel(img)  # predict on an image
#print(result[0])

# plot result
res_plotted = result[0].plot()
cv2.imshow("result", res_plotted)
cv2.waitKey(0)
