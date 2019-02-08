import cv2
import numpy as np

cv2.namedWindow("output", cv2.WINDOW_NORMAL)
cv2.resizeWindow('output',1600,600)
imgorigin=cv2.imread('123.png')
cv2.imshow('origin',imgorigin)
gray=cv2.cvtColor(imgorigin,cv2.COLOR_BGR2GRAY)
#cv2.imshow('gray',gray)
blurred = cv2.blur(gray, (5, 5))
img=cv2.threshold(blurred,150,255,cv2.THRESH_BINARY)[1]
cv2.imshow('tt1',img)
#rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 5))
#sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (8, 10))
#tophat = cv2.morphologyEx(img, cv2.MORPH_TOPHAT, rectKernel)

#gradX = cv2.Sobel(tophat, ddepth=cv2.CV_32F, dx=1, dy=0,
#                          ksize=7)

#cv2.imshow('tt',gradX)
#thresh = cv2.morphologyEx(gradX, cv2.MORPH_CLOSE, sqKernel)
# cv2.imwrite('./screencapture/detect_morpho_sq.png', thresh)
#cv2.imshow('thres',thresh)
#cv2.imwrite('test__result.png',thresh)

#mask0 = cv2.inRange(img,255,255)
#cv2.imshow("Mask0",mask0)

_,cnts,_ = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
#print(cnts)
area1 = 0.1
area2 = 500
totalDots = []

for cnt in cnts:
    mm =cv2.moments(cnt)
    print(mm)
    #print(cv2.contourArea(cnt))
    if area1 < cv2.contourArea(cnt) < area2:
        totalDots.append(cnt)

        

text = "Total number of twists are : {}".format(len(totalDots))
cv2.putText(img, text, (30,30),  cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200,200,200), 1) 
cv2.imshow("output",img)
print("Total number of twists are :{}".format(len(totalDots)))


cv2.waitKey(0)

cv2.destroyAllWindows()