import cv2
import imutils
import numpy as np
from imutils import contours

img =cv2.imread('./imgcap_s3.png')
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img = cv2.resize(img, (51, 58))
kernel = np.ones((2,2),np.uint8)
kernel2 = np.ones((45,2),np.uint8)
img2=img
rectKernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 95))
sqKernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 60))
tophat2 = cv2.morphologyEx(img,cv2.MORPH_CLOSE, rectKernel2)

'''np.seterr(divide='ignore', invalid='ignore')
gradX = cv2.Sobel(tophat2, ddepth=cv2.CV_32F, dx=0, dy=1, ksize=1)
gradX = np.absolute(gradX)
(minVal, maxVal) = (np.min(gradX), np.max(gradX))
gradX = (255 * ((gradX - minVal) / (maxVal - minVal)))
gradX = gradX.astype("uint8")

gradX = cv2.morphologyEx(gradX, cv2.MORPH_CLOSE, rectKernel2)
thresh = cv2.threshold(gradX, 0, 255,
                       cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, sqKernel2)
digitCnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                             cv2.CHAIN_APPROX_SIMPLE)
digitCnts = digitCnts[0] if imutils.is_cv2() else digitCnts[1]

try:
    digitCnts = contours.sort_contours(digitCnts,
                                       method="left-to-right")[0]
except:
    digitCnts = sorted(digitCnts, key=cv2.contourArea, reverse=True)
clone02 = np.dstack([thresh.copy()] * 3)
#tophat = cv2.morphologyEx(img, cv2.MORPH_CLOSE, rectKernel)
#tophat= cv2.morphologyEx(img, cv2.MORPH_BLACKHAT, kernel2)
#tophat2= cv2.morphologyEx(img, cv2.MORPH_BLACKHAT, kernel)'''

'''tophat = cv2.morphologyEx(img, cv2.MORPH_CLOSE, rectKernel)
tophat= cv2.erode(tophat,kernel,iterations = 3)
img2=cv2.morphologyEx(img2, cv2.MORPH_CLOSE, sqKernel)
thresh=tophat
digitCnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
digitCnts = digitCnts[0] if imutils.is_cv2() else digitCnts[1]
digitCnts2 = cv2.findContours(img2, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
digitCnts2 = digitCnts2[0] if imutils.is_cv2() else digitCnts2[1]
try:
    digitCnts = contours.sort_contours(digitCnts,
                                       method="left-to-right")[0]
except:
    digitCnts = sorted(digitCnts, key=cv2.contourArea, reverse=True)
clone02 = np.dstack([thresh.copy()] * 3)
digitCnts2 = cv2.findContours(img2, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
digitCnts2 = digitCnts2[0] if imutils.is_cv2() else digitCnts2[1]
try:
    digitCnts2 = contours.sort_contours(digitCnts2,
                                       method="left-to-right")[0]
except:
    digitCnts2 = sorted(digitCnts2, key=cv2.contourArea, reverse=True)
clone03 = np.dstack([img2] * 3)
H=0
for c in digitCnts2:
    (x, y, w, h) = cv2.boundingRect(c)
    cv2.rectangle(clone03, (x, y), (x + w, y + h), (0, 255, 0), 2)
    H=h-25 #เปลี่ยนตาม resolusion

for c in digitCnts:
    (x, y, w, h) = cv2.boundingRect(c)
    w2=H*(3/4)
    x2=x-((w2-w)/2)
    w=int(w2)
    x=int(x2)
    cv2.rectangle(clone02, (x, y), (x + w, y + h), (0, 255, 0), 2)

####'''

cv2.imshow("test",tophat2)
cv2.imwrite("./imgcap_002.png",tophat2)
#cv2.imshow("test2",tophat2)
cv2.waitKey(0)

cv2.destroyAllWindows()