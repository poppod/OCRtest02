import cv2

imgtemp =cv2.imread('./TextRef/Area1.png')
imgS=imgtemp

result = cv2.matchTemplate(imgS, imgtemp,cv2.TM_CCORR_NORMED)
(A, score, B, C) = cv2.minMaxLoc(result)
print(result)
print(score)
print(A)
print(B)
print(C)