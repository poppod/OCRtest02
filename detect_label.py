import cv2
import numpy as np
import Text_OCR
from tkinter import *








def detect(image):


  img=image
  image_center = (image.shape[0] / 2, image.shape[1] / 2)
  gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
  gradX=cv2.Sobel(gray,ddepth=cv2.CV_32F,dx=1,dy=0,ksize=-1)
  gradY=cv2.Sobel(gray,ddepth=cv2.CV_32F,dx=0,dy=1,ksize=-1)
  gradient = cv2.subtract(gradX, gradY)
  gradient = cv2.convertScaleAbs(gradient)
  Imin = np.array([0, 0,180])
  Imax = np.array([255, 255, 255])
  hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
  masks=cv2.inRange(hsv,Imin,Imax)


  blurred = cv2.blur(masks, (5, 5))
#  cv2.imshow("blur",blurred)
  (_, thresh) = cv2.threshold(blurred,20, 255, cv2.THRESH_BINARY)
  cv2.imshow("thres",thresh)

  #cv2.imshow("close",closed)
  kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 7))
  closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
  closed = cv2.erode(closed, None, iterations=4)
  closed = cv2.dilate(closed, None, iterations=4)
  cnts,_ = cv2.findContours(closed.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2:]
  cnts2, _ = cv2.findContours(gradient.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2:]
  c2 = sorted(cnts2, key=cv2.contourArea, reverse=True)[0]
  rect2 = cv2.minAreaRect(c2)
  box2 = np.intp(cv2.boxPoints(rect2))
  if len(cnts) == 0:
    box3 = box2
    return box2,cnts2
  c = sorted(cnts, key=cv2.contourArea, reverse=True)[0]
  rect = cv2.minAreaRect(c)
  box = np.intp(cv2.boxPoints(rect))
  #print(box)
  res = cv2.bitwise_and(image, image, mask=closed)
  #cv2.imshow("res", res)
  if len(cnts) == 0:
    box3=box2
  if len(cnts)!=0 :box3=box
  #cnts3=sorted(cnts3,key=cv2.contourArea,reverse=True)
  d_min = 1000
  rect_min=[[0,0],[0,0]]
  '''for contour in cnts3:
      rect = cv2.boundingRect(contour)
     # print(rect)
      #rect=cv2.minAreaRect(contour)
      if rect[3] > image.shape[1] / 2 and rect[2] > image.shape[0] / 2:
          continue
      pt1 = (rect[0], rect[1])
      c = (rect[0] + rect[2] * 1 / 2, rect[1] + rect[3] * 1 / 2)
      d = np.sqrt((c[0] - image_center[0]) ** 2 + (c[1] - image_center[1]) ** 2)
      if d < d_min:
          d_min = d
          rect_min = [pt1, (rect[2], rect[3])]'''
          #print(type(rect_min))
  rect3=cv2.boundingRect(box3)
 # if rect3[3] > image.shape[1] / 2 and rect3[2] > image.shape[0] / 2:
  #    print(rect3)
  pt1 = (rect3[0], rect3[1])
  c = (rect3[0] + rect3[2] * 1 / 2, rect3[1] + rect3[3] * 1 / 2)
  d = np.sqrt((c[0] - image_center[0]) ** 2 + (c[1] - image_center[1]) ** 2)
  if d < d_min:
      d_min = d
      rect_min = [pt1, (rect3[2], rect3[3])]

  pad = 2
  result = image[rect_min[0][1] - pad:rect_min[0][1] + rect_min[1][1] + pad,rect_min[0][0] - pad:rect_min[0][0] + rect_min[1][0] + pad]
  h, w = result.shape[:2]
  if h <= 0 or w <= 0:
      result = image

  cv2.namedWindow("crop", cv2.WINDOW_NORMAL)

  #print(text)
  cv2.imshow("crop", result)
  Text_OCR.OCR(img)
  return box,cnts
