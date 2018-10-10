import tkinter
from tkinter import *
import cv2
import threading
import PIL.Image, PIL.ImageTk
import imutils
import multiprocessing
import numpy as np
import queue
#import imu

class App():
    def __init__(self,):

        self.vs=cv2.VideoCapture(1)
        self.root=tkinter.Tk()
        self.scale()
        self.frameShow=None
        self.frame = None
        self.thread = None
        self.stopEvent = None
        self.ret,self.frameTemp=self.vs.read()
        self.frameTemp=queue.Queue()
        self.frameQ=queue.Queue()
        self.frameTemp.put(self.frameTemp)
        self.box=queue.Queue()
        self.cnts=queue.Queue()
        self.Imin0=queue.Queue()
        self.Imin1=queue.Queue()
        self.Imin2=queue.Queue()
        self.Imin0.put(0)
        self.Imin1.put(0)
        self.Imin2.put(170)
        self.panel=None
        self.panel2=None
        self.panel3=None
        self.thresh=queue.Queue()
        self.result=queue.Queue()
        self.stopEvent= threading.Event()
        self.detectThread=threading.Thread(target=self.detect,args=(self.Imin0.get(),self.Imin1.get(),self.Imin2.get()))

        self.thread=threading.Thread(target=self.videoLoop, args=())
        self.thread.start()
        self.detectThread.start()
        #self.showThread=threading.Thread(target=self.show_panel,args=())
        #self.showThread.start()
        #self.scale()
        self.root.wm_protocol("WM_DELETE_WINDOW",self.onClose)
    def videoLoop(self):

        try:
            while not self.stopEvent.is_set():
                self.ret,self.frame=self.vs.read()
                self.frameQ.put(self.frame)
                self.frameShow=imutils.resize(self.frame,width=300)
                image=cv2.cvtColor(self.frameShow,cv2.COLOR_BGR2RGB)
                image=PIL.Image.fromarray(image)
                image=PIL.ImageTk.PhotoImage(image)

                if self.panel is None:
                    self.panel=tkinter.Label(image=image)
                    self.panel.image=image
                    self.panel.pack(side="left")
                else:
                    self.panel.configure(image=image)
                    self.panel.image=image
        except RuntimeError as e:
            print("error runtime")

    def scale(self):
        self.var = IntVar()
        self.var1 = IntVar()
        self.var2 = IntVar()
        scale = Scale(self.root, from_=0, to=255, variable=self.var,command=self.scaleValue1)
        scale.set(0)
        scale1 = Scale(self.root, from_=0, to=255, variable=self.var1,command=self.scaleValue1)
        scale1.set(0)
        scale2 = Scale(self.root, from_=0, to=255, variable=self.var2,command=self.scaleValue1)
        scale2.set(180)
        scale2.pack(fill=BOTH, expand=0, side=RIGHT)
        scale1.pack(fill=BOTH, expand=0, side=RIGHT)
        scale.pack(fill=BOTH, expand=0, side=RIGHT)
    def scaleValue1(self,vk):
        self.Imin0.put(self.var.get())
        self.Imin1.put(self.var1.get())
        self.Imin2.put(self.var2.get())

    def detect(self,Imin0,Imin1,Imin2):

        try:
            while not self.stopEvent.is_set():
                ret,img = self.vs.read()

                image = img
                image_center = (image.shape[0] / 2, image.shape[1] / 2)
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                gradX = cv2.Sobel(gray, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=-1)
                gradY = cv2.Sobel(gray, ddepth=cv2.CV_32F, dx=0, dy=1, ksize=-1)
                gradient = cv2.subtract(gradX, gradY)
                gradient = cv2.convertScaleAbs(gradient)
                #Imin0 = Imin0.get()
                #Imin1 = Imin1.get()
                #Imin2 = Imin2.get()
                Imin = np.array([Imin0, Imin1, Imin2], dtype='uint8')
                Imax = np.array([255, 255, 255], dtype='uint8')
                hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
                masks = cv2.inRange(hsv, Imin, Imax)
                blurred = cv2.blur(masks, (5, 5))
                (_, thresh) = cv2.threshold(blurred, 20, 255, cv2.THRESH_BINARY)
                threshShow = imutils.resize(thresh, width=300)
                threshShow = PIL.Image.fromarray(threshShow)
                threshShow = PIL.ImageTk.PhotoImage(threshShow)
                self.thresh.put(threshShow)

                # cv2.imshow("thres", thresh)
                kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 7))
                closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
                closed = cv2.erode(closed, None, iterations=4)
                closed = cv2.dilate(closed, None, iterations=4)
                _,cnts, hierarchy = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                _,cnts2,hierarchy2 = cv2.findContours(gradient.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                c2 = sorted(cnts2, key=cv2.contourArea, reverse=True)[0]
                rect2 = cv2.minAreaRect(c2)
                box2 = np.intp(cv2.boxPoints(rect2))
                if len(cnts) == 0:
                    box3 = box2
                    self.box.put(box2)
                    self.cnts.put(cnts2)
                    # return box2, cnts2
                c = sorted(cnts, key=cv2.contourArea, reverse=True)[0]

                rect = cv2.minAreaRect(c)
                box = np.intp(cv2.boxPoints(rect))
                res = cv2.bitwise_and(image, image, mask=closed)
                if len(cnts) == 0:
                    box3 = box2
                if len(cnts) != 0: box3 = box
                d_min = 1000
                rect_min = [[0, 0], [0, 0]]
                rect3 = cv2.boundingRect(box3)
                pt1 = (rect3[0], rect3[1])
                c = (rect3[0] + rect3[2] * 1 / 2, rect3[1] + rect3[3] * 1 / 2)
                d = np.sqrt((c[0] - image_center[0]) ** 2 + (c[1] - image_center[1]) ** 2)
                if d < d_min:
                    d_min = d
                    rect_min = [pt1, (rect3[2], rect3[3])]

                pad = 2
                result = image[rect_min[0][1] - pad:rect_min[0][1] + rect_min[1][1] + pad,
                         rect_min[0][0] - pad:rect_min[0][0] + rect_min[1][0] + pad]
                h, w = result.shape[:2]
                if h <= 0 or w <= 0:
                    result = image
                result = imutils.resize(result, width=300)
                result = PIL.Image.fromarray(result)
                result = PIL.ImageTk.PhotoImage(result)
                self.result.put(result)

                # cv2.namedWindow("crop", cv2.WINDOW_NORMAL)
                # cv2.imshow("crop", result)
                self.box.put(box)
                self.cnts.put(cnts)
                thresh = self.thresh.get()
                result = self.result.get()
                if self.panel2 is None:
                    self.panel2 = (tkinter.Label(image=thresh))
                    self.panel2.image = thresh
                    self.panel2.pack(side="left")
                else:
                    self.panel2.configure(image=thresh)
                    self.panel2.image = thresh
                if self.panel3 is None:
                    self.panel3 = tkinter.Label(image=result)
                    self.panel3.image = result
                    self.panel3.pack(side="left")
                else:
                    self.panel3.configure(image=result)
                    self.panel3.image = result

        except RuntimeError as e:
            print("error runtime")

        #return box, cnts




    def onClose(self):
        self.stopEvent.set()
        #self.vs.stop()
        self.root.quit()
        exit()
        #self.root.destroy()

t=App()
t.root.mainloop()





