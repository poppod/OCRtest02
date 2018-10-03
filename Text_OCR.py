import os
import sys
import numpy as np
import cv2
try:
    import Image
except ImportError:
    from PIL import Image

from skimage.filters import threshold_local
import pytesseract
def OCR(image):

    #pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
    #tessdata_dir_config = '--tessdata-dir "C:\\Program Files\\Tesseract-OCR\\tessdata"'
    kernel = np.ones((1, 1), np.uint8)
    warped= cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

    #gray = cv2.blur(gray, (2, 4))

    #warped = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
    T = threshold_local(warped, 15, offset=12, method="gaussian")
    warped = (warped > T).astype("uint8") * 255
    #gray = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel)
    #gray = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel)
    #gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
   # ret, thresh = cv2.threshold(gray, 110, 255, 0)
    #thresh = cv2.erode(thresh, kernel, iterations=5)
    #im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #cv2.drawContours(image, contours, -1, (0, 255, 0), 3)

    cv2.imshow("gray",warped)
    #gray = cv2.blur(gray,(2,4))
   # kernel = np.ones((1, 2), np.uint8)

    #gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
    #_,gray=cv2.threshold(gray,110,255,cv2.THRESH_BINARY)

    #gray = cv2.Laplacian(gray, cv2.CV_64F)
    #gray = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel)
    #gray = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel)
    #cv2.imshow("gray", gray*-255)
    #final=pytesseract.image_to_string(Image.fromarray(thresh,mode='P'),lang='eng',config=tessdata_dir_config)
    #print(final)

    #kernel = np.ones((2, 1), np.uint8)
    #gray = cv2.erode(gray, kernel, iterations=1)
    #gray = cv2.dilate(gray, kernel, iterations=1)
   # gray = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel)
   # filename = "{}.png".format(os.getpid())
    #cv2.imwrite(filename, gray)
    #gray=cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY, 11, 2)
    #text = pytesseract.image_to_string(Image.open(filename),"eng")
    #os.remove(filename)
    #print(text)
   # text=pytesseract.image_to_string(Image.Re(gray,'r'),"eng")
    #print(text)
