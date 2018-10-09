from tkinter import *

import tkinter
from multiprocessing import pool
import multiprocessing
import queue
import time
import detect_label
import tkinter
from tkinter import ttk
from tkinter import messagebox
import threading
import cv2
print(tkinter.TkVersion)
import numpy as np

class window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.n = int
        self.master = master
        self.init_window()
        #self.input_value()

    def init_window(self):
        self.pack(fill=BOTH, expand=1)
        self.var = IntVar()
        self.var1 = IntVar()
        self.var2 = IntVar()

        self.L1 = Label(self)
        self.L2 = Label(self, text="m")
        self.L3 = Label(self, text="m")

        self.L1.place(x=50, y=0)
        self.L2.place(x=200, y=0)
        self.L3.place(x=350, y=0)
        self.L1.pack()
        self.L2.pack()
        self.L3.pack()


        scale = Scale(self, from_=0, to=255, variable=self.var,command = self.show)
        scale.set(0)
        scale1 = Scale(self, from_=0, to=255, variable=self.var1,command = self.show)
        scale1.set(0)
        scale2 = Scale(self, from_=0, to=255, variable=self.var2,command = self.show)
        scale2.set(180)
        scale.pack(fill=BOTH, expand=1,side=LEFT)
        scale1.pack(fill=BOTH, expand=1,side=RIGHT)
        scale2.pack(fill=BOTH, expand=1, side=RIGHT)
        #b1=Button(self,text = "Get Scale Value")
        #b1.place(x=200,y=200)

    def show(self,vk):
        selection=str(self.var.get())
        selection1=str(self.var1.get())
        selection2=str(self.var2.get())
        self.L1.configure(text=selection)
        self.L2.configure(text=selection1)
        self.L3.configure(text=selection2)
        lock.acquire()

        scaleValue1.put(int(self.var.get()))
        scaleValue2.put(int(self.var1.get()))
        scaleValue3.put(int(self.var2.get()))
        scaleArr[0]=scaleValue1.get()
        scaleArr[1]=scaleValue2.get()
        scaleArr[2]=scaleValue3.get()
        lock.release()


        #camera_start(int(self.var.get()),int(self.var1.get()),int(self.var2.get()))

        #Mt1.join()
        #print(str(self.var.get()))


def camera_start(Imin1, Imin2, Imin3):
    #img=None
    lock = multiprocessing.Lock()
    q1 = multiprocessing.Queue()
    q2 = multiprocessing.Queue()
    frame=multiprocessing.Queue()
    frame.put(None)
    camera_selectProcess = multiprocessing.Process(target=detect, args=(frame, Imin1, Imin2, Imin3, q1, q2,))
    camera = cv2.VideoCapture(1)
    camera_selectProcess.start()
    #threading.Thread(target=detect())
    while True:
        (ret, frameImg) = camera.read()
        # image = frame
        frame.put(frameImg)
        if not ret:
            break
       #threading.Thread(target=detect(frame, Imin1, Imin2, Imin3,q1,q2)).start()
        #lock.acquire()
        box=q1.get()
        contours=q2.get()
        #lock.release()
        #box,contours=detect(frame, Imin1, Imin2, Imin3,q1,q2)
       # box=q1.get()
        #contours=q2.get()

            #p.close()
        # print( __name__ )
        # image_center = (image.shape[0] / 2, image.shape[1] / 2)
        cv2.drawContours(frame, [box], -1, (0, 255, 0), thickness=2)

        cv2.imshow("Frame", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break


    # cv2.cv2.drawContours()
    camera.release()
    cv2.destroyAllWindows()
def detect(image,Imin1,Imin2,Imin3,q1,q2):

  if image == None :
      image=cv2.imread("6904.png")
  img=image
  image_center = (image.shape[0] / 2, image.shape[1] / 2)
  gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
  gradX=cv2.Sobel(gray,ddepth=cv2.CV_32F,dx=1,dy=0,ksize=-1)
  gradY=cv2.Sobel(gray,ddepth=cv2.CV_32F,dx=0,dy=1,ksize=-1)
  gradient = cv2.subtract(gradX, gradY)
  gradient = cv2.convertScaleAbs(gradient)
  Imin = np.array([Imin1,Imin2,Imin3])
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
  #Text_OCR.OCR(img)
  q1.put(box)
  q2.put(cnts)
  return box,cnts

def config_start():
    root = Tk()
    root.geometry("400x300")
    app = window(root)
    app.mainloop()

if __name__ == "__main__":
    scaleArr=multiprocessing.Array('i',3)
    scaleValue1=multiprocessing.Queue()
    scaleValue2=multiprocessing.Queue()
    scaleValue3=multiprocessing.Queue()
    cameraProcess = multiprocessing.Process(target=camera_start, args=(scaleArr[0], scaleArr[1], scaleArr[2],))
    cameraProcess.start()
    lock=multiprocessing.Lock()

    config_start()

    #scaleProcess.start()
    #camera_selectProcess.start()



