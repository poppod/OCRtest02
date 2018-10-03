import numpy as np
import cv2
import detect_label
camera=cv2.VideoCapture(1)
while True :
    (ret,frame)=camera.read()
   # image = frame

    if not ret:
        break
  
    box,contours=detect_label.detect(frame)
    #image_center = (image.shape[0] / 2, image.shape[1] / 2)


    cv2.drawContours(frame,[box],-1,(0,255,0),thickness=2)


    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    #cv2.cv2.drawContours()
camera.release()
cv2.destroyAllWindows()