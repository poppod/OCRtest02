import cv2
import numpy as np

camera = cv2.VideoCapture(1)
def makeLow():
    camera.set(3,640)
    camera.set(4,240)
    camera.set(5,60)

while True:
    (ret, frame) = camera.read()
    # image = frame

    if not ret:
        break


    # image_center = (image.shape[0] / 2, image.shape[1] / 2)

    

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    # cv2.cv2.drawContours()
camera.release()
cv2.destroyAllWindows()