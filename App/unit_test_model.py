from Model import Model
import cv2

img_KO = cv2.imread("image_KO.png", 0)
img_OK = cv2.imread("image_OK.png", 0)

model = Model()

print("prediction KO")
print(model.predict(img_KO))
print("prediction OK")
print(model.predict(img_OK))
