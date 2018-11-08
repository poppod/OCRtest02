import tkinter
import time
from tkinter import *
import cv2
import threading
import PIL.Image, PIL.ImageTk
import imutils
import multiprocessing
import numpy as np
import queue
from imutils import contours
from skimage.filters import threshold_local
#import imu

class App():
    def __init__(self,):

        self.vs=cv2.VideoCapture(0)
        self.root=tkinter.Tk()
        self.scale()
        self.scale2()
        self.frameShow=None
        self.frame1=None
        self.frame = None
        self.thread = None
        self.stopEvent = None
        self.ret,self.frameTemp=self.vs.read()
        self.frameTemp=queue.Queue()
        self.frameQ=queue.Queue()
        self.frameTemp.put(self.frameTemp)
        self.box=queue.Queue()
        self.cnts=queue.Queue()
        self.imgOrigin = None

        self.lock=threading.Lock()
        self.TextOcrRef()
        self.panel=None
        self.panel2=None
        self.panel3=None
        self.panel4=None
        self.panel5=None
        self.panel6=None #not use
        self.buttom=None
        self.thresh=queue.Queue()
        self.result=queue.Queue()
        self.stopEvent= threading.Event()


        self.thread=threading.Thread(target=self.videoLoop, args=())
        self.thread.daemon=True
        self.thread.start()


        self.TextocrThread = threading.Thread(target=self.TextOCR, args=())
        self.TextocrThread.daemon=True
        self.TextocrThread.start()

        #self.showThread=threading.Thread(target=self.show_panel,args=())
        #self.showThread.start()
        #self.scale()
        #self.TextOCR()

        self.root.wm_protocol("WM_DELETE_WINDOW",self.onClose)
    def videoLoop(self):
        self.ret, self.frame = self.vs.read()
        self.detectThread = threading.Thread(target=self.detect, args=())
        self.detectThread.daemon = True
        self.detectThread.start()

        try:
            while not self.stopEvent.is_set():
                self.ret,self.frame=self.vs.read()
                #self.frameQ.put(self.frame)
                self.frameShow=imutils.resize(self.frame,width=150)
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
            self.vs.release()


    def scale(self):
        self.var = IntVar()
        self.var1 = IntVar()
        self.var2 = IntVar()
        scale = Scale(self.root, from_=0, to=255, variable=self.var)
        scale.set(0)
        scale1 = Scale(self.root, from_=0, to=255, variable=self.var1)
        scale1.set(0)
        scale2 = Scale(self.root, from_=0, to=255, variable=self.var2)
        scale2.set(86)
        scale2.pack(fill=BOTH, expand=0, side=RIGHT)
        scale1.pack(fill=BOTH, expand=0, side=RIGHT)
        scale.pack(fill=BOTH, expand=0, side=RIGHT)

    def scale2(self):
        self.varMax=IntVar()
        self.varMax2=IntVar()
        self.varMax3=IntVar()
        self.varMax4=IntVar()
        scale = Scale(self.root, from_=0, to=255, variable=self.varMax)
        scale.set(255)
        scale1 = Scale(self.root, from_=0, to=255, variable=self.varMax2)
        scale1.set(255)
        scale2 = Scale(self.root, from_=0, to=255, variable=self.varMax3)
        scale2.set(255)
        scale3=Scale(self.root,from_=0, to=255,variable=self.varMax4,orient=tkinter.HORIZONTAL)
        scale3.set(90)
        scale3.pack(fill=BOTH, expand=0, side=RIGHT)
        scale2.pack(fill=BOTH, expand=0, side=RIGHT)
        scale1.pack(fill=BOTH, expand=0, side=RIGHT)
        scale.pack(fill=BOTH, expand=0, side=RIGHT)


    def detect(self):

        while not self.stopEvent.is_set():
                #ret,img= self.vs.read()
                #img=self.frame

                image = self.frame
                image_center = (image.shape[0] / 2, image.shape[1] / 2)
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                gradX = cv2.Sobel(gray, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=-1)
                gradY = cv2.Sobel(gray, ddepth=cv2.CV_32F, dx=0, dy=1, ksize=-1)
                gradient = cv2.subtract(gradX, gradY)
                gradient = cv2.convertScaleAbs(gradient)
                #Imin0 = self.Imin0.get()
                #Imin1 = self.Imin1.get()
                #Imin2 = self.Imin2.get()
                Imin = np.array([self.var.get(), self.var1.get(),self.var2.get()], dtype='uint8')
                Imax = np.array([255,255, 255], dtype='uint8')
                hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
                masks = cv2.inRange(hsv, Imin, Imax)
                blurred = cv2.blur(masks, (1, 1))



                (_, thresh) = cv2.threshold(blurred, 180, 255, cv2.THRESH_BINARY_INV)

                rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 30))
                sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
                tophat = cv2.morphologyEx(thresh, cv2.MORPH_TOPHAT, rectKernel)

                gradX = cv2.Sobel(tophat, ddepth=cv2.CV_64F, dx=1, dy=0,
                                  ksize=7)
                gradX = np.absolute(gradX)
                (minVal, maxVal) = (np.min(gradX), np.max(gradX))
                gradX = (255 * ((gradX - minVal) / (maxVal - minVal)))
                gradX = gradX.astype("uint8")

                gradX = cv2.morphologyEx(gradX, cv2.MORPH_CLOSE, rectKernel)
                thresh = cv2.threshold(gradX, 0, 255,
                                       cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
                thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, sqKernel)



                threshShow = imutils.resize(thresh, width=200)
                threshShow = PIL.Image.fromarray(threshShow)
                threshShow = PIL.ImageTk.PhotoImage(threshShow)
                #self.lock.acquire()
                #self.thresh.put(threshShow)
                #self.lock.release()
                # cv2.imshow("thres", thresh)
                kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (55, 57))
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
                    cnts=cnts2
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

                pad = 20
                result = image[rect_min[0][1] - pad:rect_min[0][1] + rect_min[1][1] + pad,
                         rect_min[0][0] - pad:rect_min[0][0] + rect_min[1][0] + pad]
                h, w = result.shape[:2]
                if h <= 0 or w <= 0:
                    result = image

                #print(result.shape[:2])

                self.imgOrigin=result

                result = imutils.resize(result, width=300,height=200)
                result = PIL.Image.fromarray(result)
                result = PIL.ImageTk.PhotoImage(result)

                #self.lock.acquire()
                #self.result.put(result)
                #self.lock.release()
                # cv2.namedWindow("crop", cv2.WINDOW_NORMAL)
                # cv2.imshow("crop", result)
                self.box.put(box)
                self.cnts.put(cnts)
                #thresh1 = self.thresh.get()
                #result1 = self.result.get()
                if self.panel2 is None:
                    self.panel2 = (tkinter.Label(image=threshShow))
                    self.panel2.image = threshShow
                    self.panel2.pack(side="bottom")
                else:
                    self.panel2.configure(image=threshShow)
                    self.panel2.image = threshShow
                if self.panel3 is None:
                    self.panel3 = tkinter.Label(image=result)
                    self.panel3.image = result
                    self.panel3.pack(side="bottom")


                else:
                    self.panel3.configure(image=result)
                    self.panel3.image = result





        #return box, cnts




    def onClose(self):
        self.stopEvent.set()
        #self.vs.release()
        self.root.quit()
        #self.root.q
        #exit()
        #self.root.destroy()

    def TextOcrRef(self):
        ref=cv2.imread("./TextRef/temp.png",0)
        ref = cv2.threshold(ref, 200, 255, cv2.THRESH_BINARY_INV)[1]
        cv2.imshow('ref', ref)
        refCnt = cv2.findContours(ref.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        refCnt = refCnt[0] if imutils.is_cv2() else refCnt[1]
        refCnt = contours.sort_contours(refCnt, method="left-to-right")[0]
        self.digits = {}
        self.roi = {}
        for (i, c) in enumerate(refCnt):
            (x, y, w, h) = cv2.boundingRect(c)
            x -= 12
            y -= 12
            w += 20
            h += 20
            self.roi[i] = ref[y:y + h, x:x + w]
            self.roi[i] = cv2.resize(self.roi[i], (57, 88))
            # cv2.imwrite("roi"+str(i)+'o.png',roi)
            self.digits[i] = self.roi[i]

        clone = np.dstack([ref.copy()] * 3)
        for c in refCnt:
            (x, y, w, h) = cv2.boundingRect(c)

            cv2.rectangle(clone, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # roi = ref[y:y + h, x:x + w]
        #cv2.imshow("Simple Method", clone)
        cv2.imshow('roi', self.roi[10])
        #cv2.imshow("test",ref)
    def TextOCR(self):
        rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 10))
        sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
        while not self.stopEvent.is_set():
            if not self.imgOrigin is None:
                imgOrigin=self.imgOrigin
                #imgOrigin = imutils.resize(imgOrigin, width=150)

                gray = cv2.cvtColor(imgOrigin, cv2.COLOR_BGR2GRAY)
                #tophat = cv2.morphologyEx(gray, cv2.MORPH_TOPHAT, rectKernel)
                Imin = np.array([self.var.get(), self.var1.get(), self.varMax4.get()], dtype='uint8')
                Imax = np.array([self.varMax.get(), self.varMax2.get(), self.varMax2.get()], dtype='uint8')
                hsv = cv2.cvtColor(imgOrigin, cv2.COLOR_BGR2HSV)
                masks = cv2.inRange(hsv, Imin, Imax)
                blurred = cv2.blur(masks, (1, 1))
                img = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV)[1]
                #img = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)
                #img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                imgfilter=cv2.bilateralFilter(gray,8, 17, 17)
                gray=imgfilter
                #imgfilter = cv2.blur(imgfilter, (1, 1))
                #img=imgfilter
                #img= cv2.Canny(img, 30,108)





                T = threshold_local(gray, 25, offset=6, method="gaussian")
                imgWrap = (gray > T).astype("uint8") * 255
                imgWrap = cv2.threshold(imgWrap, 200, 255, cv2.THRESH_BINARY_INV)[1]
                #img=imgWrap
                imgTocrop=imgWrap
                '''img = imutils.resize(img, width=300, height=200)
                img = PIL.Image.fromarray(img)
                img = PIL.ImageTk.PhotoImage(img)
                if self.panel4 is None:
                    self.panel4 = tkinter.Label(image=img)
                    self.panel4.image = img
                    self.panel4.pack(side="left")


                else:
                    self.panel4.configure(image=img)
                    self.panel4.image = img
                #cv2.imshow("test",imgOrigin)

                #cv2.imshow("kk", img)'''

                tophat = cv2.morphologyEx(img, cv2.MORPH_TOPHAT, rectKernel)
                img2=img
                np.seterr(divide='ignore', invalid='ignore')
                gradX = cv2.Sobel(tophat, ddepth=cv2.CV_64F, dx=1, dy=0,ksize=7)
                gradX = np.absolute(gradX)
                (minVal, maxVal) = (np.min(gradX), np.max(gradX))
                gradX = (255 * ((gradX - minVal) / (maxVal - minVal)))
                gradX = gradX.astype("uint8")

                gradX = cv2.morphologyEx(gradX, cv2.MORPH_CLOSE, rectKernel)
                thresh = cv2.threshold(gradX, 0, 255,
                                       cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
                thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, sqKernel)
                cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                        cv2.CHAIN_APPROX_SIMPLE)
                cnts = cnts[0] if imutils.is_cv2() else cnts[1]
                cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
                #cnts = contours.sort_contours(cnts, method="top-to-buttom")[0]
                locs = []
                tmpcnts = {}
                clone01 = np.dstack([thresh.copy()] * 3)

                #cnts2 = cv2.findContours(clone01.copy(), cv2.RETR_EXTERNAL,
                #                        cv2.CHAIN_APPROX_SIMPLE)
                #cnts2 = cnts2[0] if imutils.is_cv2() else cnts2[1]
                #cnts2 = sorted(cnts2, key=cv2.contourArea, reverse=True)
                font = cv2.FONT_HERSHEY_SIMPLEX

                for (idx, c) in enumerate(cnts):
                    x, y, w, h = cv2.boundingRect(c)
                    x-=5
                    y-=5
                    w+=5
                    h+=5
                    #h=h+5
                    cv2.rectangle(clone01, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    tmpcnts[idx] = imgTocrop[y:y + h, x:x + w]
                    #

                    locs.append((x, y, w, h))

                locs = sorted(locs, key=lambda X: X[0])


                img = clone01
                img = imutils.resize(img, width=300, height=200)
                img = PIL.Image.fromarray(img)
                img = PIL.ImageTk.PhotoImage(img)
                if self.panel4 is None:
                    self.panel4 = tkinter.Label(image=img)
                    self.panel4.image = img
                    self.panel4.pack(side="bottom")
                else:
                    self.panel4.configure(image=img)
                    self.panel4.image = img
                output = []
                kernel = np.ones((1, 1), np.uint8)
                kernel2 = np.ones((2, 5), np.uint8)
                try:
                    tmpcnts[0] = cv2.blur(tmpcnts[0], (1, 1))
                    #tmpcnts[0] = cv2.dilate(tmpcnts[0], kernel, iterations=1)
                    tmpcnts[0] =cv2.morphologyEx(tmpcnts[0], cv2.MORPH_OPEN, kernel)
                    tmpcnts[0] = cv2.morphologyEx(tmpcnts[0], cv2.MORPH_CLOSE, kernel2)
                except : print("tmp error");continue
                img=tmpcnts[0]
                #print(tmpcnts[1].shape[:2])
                ##########test#######
                '''for i in tmpcnts:
                    if i==0 :
                        digitCnts=10
                    elif i== 1 :
                        digitCnts=8
                    elif i==2 :
                        digitCnts=1

                    print(i)
                    x,y=0,0
                    for c in range(digitCnts):
                        #(x, y, w, h) = cv2.boundingRect(c)
                        h,w=tmpcnts[i].shape[:2]
                        roi = tmpcnts[i][y:y + h, x:x + int(w/digitCnts)]
                        #roi = cv2.resize(roi, (57, 88))
                        img=roi
                        #img = imutils.resize(img, width=300, height=200)
                        img = PIL.Image.fromarray(img)
                        img = PIL.ImageTk.PhotoImage(img)
                        if self.panel5 is None:
                            self.panel5 = tkinter.Label(image=img)
                            self.panel5.image = img
                            self.panel5.pack(side="left")
                        else:
                            self.panel5.configure(image=img)
                            self.panel5.image = img

                        #y+=h
                        x+=int(w/digitCnts)
                        time.sleep(0.5)


                ####################'''
                TestCnts= cv2.findContours(tmpcnts[0].copy(), cv2.RETR_EXTERNAL,
                                             cv2.CHAIN_APPROX_SIMPLE)
                TestCnts = TestCnts[0] if imutils.is_cv2() else TestCnts[1]
                TestCnts = sorted(TestCnts, key=cv2.contourArea, reverse=True)
                img = np.dstack([tmpcnts[0].copy()] * 3)
                for (idx, c) in enumerate(TestCnts):
                    x, y, w, h = cv2.boundingRect(c)

                    #h=h+5
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                #cv2.drawContours(img, TestCnts, -1, (0, 255, 0), 3)
                img = imutils.resize(img, width=300, height=200)
                img = PIL.Image.fromarray(img)
                img = PIL.ImageTk.PhotoImage(img)
                if self.panel5 is None:
                    self.panel5 = tkinter.Label(image=img)
                    self.panel5.image = img
                    self.panel5.pack(side="left")
                else:
                    self.panel5.configure(image=img)
                    self.panel5.image = img

                '''for (i, (gX, gY, gW, gH)) in enumerate(locs):

                    groupOutput = []
                    #digitCnts = cv2.findContours(tmpcnts[i].copy(), cv2.RETR_EXTERNAL,
                    #                             cv2.CHAIN_APPROX_SIMPLE)
                   # digitCnts = digitCnts[0] if imutils.is_cv2() else digitCnts[1]
                    #digitCnts = sorted(digitCnts, key=cv2.contourArea, reverse=True)
                    if i==0 :
                        digitCnts=10
                    elif i== 1 :
                        digitCnts=8
                    elif i==2 :
                        digitCnts=1

                    print(i)
                    x,y=0,0
                    for c in range(digitCnts):
                        #(x, y, w, h) = cv2.boundingRect(c)
                        h,w=tmpcnts[i].shape[:2]
                        roi = tmpcnts[i][y:y + h, x:x + int(w/digitCnts)]
                        try: roi = cv2.resize(roi, (57, 88))
                        except: print("resize error");continue
                        img=roi
                        #img = imutils.resize(img, width=300, height=200)
                        img = PIL.Image.fromarray(img)
                        img = PIL.ImageTk.PhotoImage(img)
                        if self.panel5 is None:
                            self.panel5 = tkinter.Label(image=img)
                            self.panel5.image = img
                            self.panel5.pack(side="left")
                        else:
                            self.panel5.configure(image=img)
                            self.panel5.image = img

                        #y+=h
                        x+=int(w/digitCnts)
                        time.sleep(0.5)

                        #cv2.imshow("roi", roi)
                        scores = []
                        for (digit, digitROI) in self.digits.items():
                            # apply correlation-based template matching, take the
                            # score, and update the scores list
                            result = cv2.matchTemplate(roi, digitROI,
                                                       cv2.TM_CCOEFF)
                            (_, score, _, _) = cv2.minMaxLoc(result)
                            scores.append(score)
                        if int(np.argmax(scores)) > 9:
                            if int(np.argmax(scores)) == 10:
                                groupOutput.append('/')
                            elif int(np.argmax(scores)) == 11:
                                groupOutput.append('A')
                            elif int(np.argmax(scores)) == 12:
                                groupOutput.append('B')
                            elif int(np.argmax(scores)) == 13:
                                groupOutput.append('C')
                        else:
                            groupOutput.append(str(np.argmax(scores)))
                        print(groupOutput)



                    cv2.rectangle(imgOrigin, (gX - 5, gY - 5),
                                  (gX + gW + 5, gY + gH + 5), (0, 255, 0), 2)
                    cv2.putText(imgOrigin, "".join(groupOutput), (gX, gY - 15),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 2)

                    # update the output digits list
                    #print(output)
                    output.extend(groupOutput)

                print("number  #: {}".format("".join(output)))
                #cv2.imshow("Image", imgOrigin)'''



t=App()
t.root.mainloop()





