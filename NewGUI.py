import tkinter
import time
import os
import io
from tkinter import *
from tkinter import filedialog,messagebox

import pytesseract
import cv2
import threading
import PIL.Image, PIL.ImageTk
import imutils
import multiprocessing
import numpy as np
import queue

from itertools import product
from imutils import contours
from multiprocessing.pool import ThreadPool
from skimage.filters import threshold_local
#import imu

class App():
    def __init__(self,):

        self.vs=cv2.VideoCapture(0)
        self.root=tkinter.Tk()
        #self.scale()
        #self.scale2()
        self.Detect_flag=0
        self.frameShow=None
        self.frame1=None
        self.frame = None
        self.thread = None
        self.stopEvent = None
        self.ret,self.frameTemp=self.vs.read()
        self.MultiOcr=None
        self.ClickValue=0

        self.varMax = IntVar()
        self.varMax2 = IntVar()
        self.varMax3 = IntVar()
        self.varMax4 = IntVar()
        self.varMax5 = IntVar()

        self.var = IntVar()
        self.var1 = IntVar()
        self.var2 = IntVar()

        self.rectY = IntVar()
        self.rectX = IntVar()
        self.sqY = IntVar()
        self.sqX = IntVar()
        self.rectY2 = IntVar()
        self.rectX2 = IntVar()
        self.sqY2 = IntVar()
        self.sqX2 = IntVar()
        self.treshImg=None
        self.ImgCap=None

        self.HeightBbox=None
        self.WeightBbox=None

        #self.box=queue.Queue()
        #self.cnts=queue.Queue()
        self.imgOrigin = None

        self.lock=multiprocessing.Lock()
        #self.TextOcrRef()
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

        self.page1_selectOption()

        '''self.thread=threading.Thread(target=self.videoLoop, args=())
        self.thread.daemon=True
        self.thread.start()'''


        '''self.TextocrThread = threading.Thread(target=self.TextOCR, args=())
        self.TextocrThread.daemon=True
        self.TextocrThread.start()'''

        '''self.detectThread = threading.Thread(target=self.detect, args=())
        self.detectThread.daemon = True
        self.detectThread.start()'''

        #self.multi_OCR()
        #self.showThread=threading.Thread(target=self.show_panel,args=())
        #self.showThread.start()
        #self.scale()
        #self.TextOCR()

        self.root.wm_protocol("WM_DELETE_WINDOW",self.onClose)
    def Save_Bbox(self,h,w):
        self.HeightBbox=h
        self.WeightBbox=w
    def Click_ValueBbox(self):
        self.ClickValue=5
    def settingButton(self):
        #self.ClickValue+=1
        self.page2_selectFile()

    def page1_selectOption(self):
        self.root.geometry('800x480')
        self.root.title("Start page")
        defaultButton=Button(self.root,text='Default',command=self.default_process_solution_1).grid(row=1,column=1,columnspan=2, rowspan=2,sticky=W+N+E+S)
        setingtButton = Button(self.root, text='Setting',command=self.settingButton).grid(row=1, column=3,columnspan=2, rowspan=2,sticky=W+N+E+S)

    def openDialog(self):
        self.filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                                   filetypes=(("*jpg files", "*.jpg"), ("*png files", "*.png")))
        self.importImg()
    def Show_panel01_0_0(self,img):
        try: img = imutils.resize(img, width=150, height=100)
        except: img=img
        img = PIL.Image.fromarray(img)
        img = PIL.ImageTk.PhotoImage(img)
        if self.panel is None:
            self.panel = tkinter.Label(image=img)
            self.panel.image = img
            self.panel.grid(row=0, column=0)
        else:
            self.panel.configure(image=img)
            self.panel.image = img

    def Show_panel02_0_1(self,img):
        try: img = imutils.resize(img, width=150, height=100)
        except: img=img
        img = PIL.Image.fromarray(img)
        img = PIL.ImageTk.PhotoImage(img)
        if self.panel2 is None:
            self.panel2 = tkinter.Label(image=img)
            self.panel2.image = img
            self.panel2.grid(row=0, column=1)
        else:
            self.panel2.configure(image=img)
            self.panel2.image = img
    def Show_panel03_1_0(self,img):
        try: img = imutils.resize(img, width=150, height=100)
        except: img=img
        img = PIL.Image.fromarray(img)
        img = PIL.ImageTk.PhotoImage(img)
        if self.panel3 is None:
            self.panel3 = tkinter.Label(image=img)
            self.panel3.image = img
            self.panel3.grid(row=1, column=0)
        else:
            self.panel3.configure(image=img)
            self.panel3.image = img
    def Show_panel04_1_1(self,img):
        try: img = imutils.resize(img, width=150, height=100)
        except: img=img
        img = PIL.Image.fromarray(img)
        img = PIL.ImageTk.PhotoImage(img)
        if self.panel4 is None:
            self.panel4 = tkinter.Label(image=img)
            self.panel4.image = img
            self.panel4.grid(row=1, column=1)
        else:
            self.panel4.configure(image=img)
            self.panel4.image = img
    def Show_panel05_2_0(self,img):
        try: img = imutils.resize(img, width=150, height=100)
        except: img=img
        img = PIL.Image.fromarray(img)
        img = PIL.ImageTk.PhotoImage(img)
        if self.panel5 is None:
            self.panel5 = tkinter.Label(image=img)
            self.panel5.image = img
            self.panel5.grid(row=2, column=0)
        else:
            self.panel5.configure(image=img)
            self.panel5.image = img
    def importImg(self):
        #img=PIL.Image.open(self.filename)
        MegLabel=StringVar()

        img = cv2.imread(self.filename)

        try:
            img2=img
            self.Show_panel01_0_0(img)
        except:
            self.panel=None
            Nonelabel = Label(self.root, text="<<<<None Image Choose file(agian) Please>>>").grid(row=0,column=0)

        if self.panel is None:

            Nonelabel=Label(self.root,textvariable=MegLabel).grid(row=1,column=1)
            MegLabel.set("None")
        else:
            fileImportButton = Button(self.root, text="Import",command=lambda : self.Save_tempImg(img2)).grid(row=0,column=2)
            MegLabel.set("Get Image")
            #Nonelabel.destroy()
            Getlabel = Label(self.root,textvariable=MegLabel).grid(row=1, column=1)

    def Save_tempImg(self,img):
        error=0
        Msg=messagebox.askyesno("Import and Install ROI","Do you want to Import and install ROI")
        if Msg == True:
            if img is None :
                NoImportLabel = Label(self.root, text="You do not import Image and install ROI(use default)").grid(
                    row=1, column=1)
            else:
                cv2.imwrite('./TextRef/temp.png', img=img)  # chang to temp.png
            try:
                self.TextOcrRef()
                error=0
            except:
                messagebox.showerror(title="File Error",message="File Error Import new file")
                error=1

        else:
            NoImportLabel=Label(self.root,text="You do not import Image and install ROI(use default)").grid(row=1,column=1)
            self.TextOcrRef()
        if error==0 :
            OkNextButton=Button(self.root,text="OK and Next",command=self.page3_SettingVSCAP).grid(row=2,column=2)

    def Reset_Bbox(self):
        self.HeightBbox=None
        self.WeightBbox=None
    def page3_SettingVSCAP(self):
        self.panel=None
        for ele in self.root.winfo_children():
            ele.destroy()
        self.root.title("Setting Video Capture")
        self.scale()
        self.scale4()
        self.thread = threading.Thread(target=self.videoLoop, args=())
        self.thread.daemon = True
        self.thread.start()

        BboxSaveButton = Button(self.root, text="Target Area", command=self.Click_ValueBbox).grid(row=1, column=2)
        ResetBboxSaveButton = Button(self.root, text="Reset", command=self.Reset_Bbox).grid(row=2, column=2)
        OkNextButton = Button(self.root, text="OK and Next", command=self.page3_To_page4).grid(row=3, column=3)
    def page3_To_page4(self):
        Msg=messagebox.askyesno("Save and Next","Save target Area and Other setting")
        if Msg==True:
            self.panel = None
            Area_configre_H=open('./Configure/AreaH.txt',"w")
            Area_configre_H.write(str(self.HeightBbox))
            Area_configre_H.close()
            Area_configre_W=open('./Configure/AreaW.txt',"w")
            Area_configre_W.write(str(self.WeightBbox))
            Area_configre_W.close()
            B_scale=open('./Configure/B_scale.txt',"w")
            B_scale.write(str(self.var.get()))
            B_scale.close()
            G_scale=open('./Configure/G_scale.txt',"w")
            G_scale.write(str(self.var1.get()))
            G_scale.close()
            R_scale=open('./Configure/R_scale.txt',"w")
            R_scale.write(str(self.var2.get()))
            R_scale.close()

            rectY2 = open('./Configure/rectY2.txt', 'w')
            rectY2.write(str(self.rectY2.get()))
            rectY2.close()
            rectX2 = open('./Configure/rectX2.txt', 'w')
            rectX2.write(str(self.rectX2.get()))
            rectX2.close()
            sqY2 = open('./Configure/sqY2.txt', 'w')
            sqY2.write(str(self.sqY2.get()))
            sqY2.close()
            sqX2 = open('./Configure/sqX2.txt', 'w')
            sqX2.write(str(self.sqX2.get()))
            sqX2.close()
            self.ClickValue=2
            self.page4_settingDigit()

    def page4_settingDigit(self):
        self.ClickValue = 2
        for ele in self.root.winfo_children():
            ele.destroy()
        self.panel=None
        self.panel2=None
        self.panel3=None
        if self.thread.isAlive() ==True :
            print("thread Alive")
            self.scale2()
            self.scale3()
            #self.scale4()
            '''self.TextocrThread = threading.Thread(target=self.TextOCR, args=())
            self.TextocrThread.daemon = True
            self.TextocrThread.start()'''
            OkNextButton = Button(self.root, text="OK and Next", command=self.page4_To_page5).grid(row=3, column=3)

        else:
            print("dead")
    def page4_To_page5(self):

        Msg = messagebox.askyesno("Save and Next", "Save Value and Other setting")
        if Msg == True:
            self.ClickValue = 3
            B_scale2 = open('./Configure/B_scale2.txt', "w")
            B_scale2.write(str(self.varMax.get()))
            B_scale2.close()
            G_scale2=open('./Configure/G_scale2.txt', "w")
            G_scale2.write(str(self.varMax2.get()))
            G_scale2.close()
            R_scale2=open('./Configure/R_scale2.txt', "w")
            R_scale2.write(str(self.varMax3.get()))
            R_scale2.close()
            R_scale2_min_for_Imgtocrop=open('./Configure/R_scale2_for_Imgtocrop.txt', "w")
            R_scale2_min_for_Imgtocrop.write(str(self.varMax4.get()))
            R_scale2_min_for_Imgtocrop.close()
            R_scale2_min_for_ImgWarp=open('./Configure/R_scale2_for_ImgWarp.txt', "w")
            R_scale2_min_for_ImgWarp.write(str(self.varMax5.get()))
            R_scale2_min_for_ImgWarp.close()
            '''self.rectY = IntVar()
            self.rectX = IntVar()
            self.sqY = IntVar()
            self.sqX = IntVar()'''
            rectY=open('./Configure/rectY.txt','w')
            rectY.write(str(self.rectY.get()))
            rectY.close()
            rectX=open('./Configure/rectX.txt','w')
            rectX.write(str(self.rectX.get()))
            rectX.close()
            sqY=open('./Configure/sqY.txt','w')
            sqY.write(str(self.sqY.get()))
            sqY.close()
            sqX=open('./Configure/sqX.txt','w')
            sqX.write(str(self.sqX.get()))
            sqX.close()
            self.ClickValue=3
            self.page5_Insert_Value()
    def load_default_value(self):
        Date_value = open('./Configure/Date_value.txt', "r")

        self.Value1_Entry.insert(END,str(Date_value.read()))
        Date_value.close()
        Number_value = open('./Configure/Number_value.txt', "r")
        self.Value2_Entry.insert(END,str(Number_value.read()))
        Number_value.close()
        Code_value = open('./Configure/Code_value.txt', "r")
        self.Value3_Entry.insert(END, str(Code_value.read()))
        Code_value.close()

    def page5_Insert_Value(self):
        self.ClickValue = 3
        self.root.title("Insert Value")
        self.DateValue=StringVar()
        self.NcodeValue=StringVar()
        self.CcodeValue=StringVar()
        self.ClickValue = 3

        for ele in self.root.winfo_children():
            ele.destroy()
        self.panel = None
        self.panel2 = None
        self.panel3 = None
        self.panel4 = None
        Button(self.root, text="Default load", command=self.load_default_value).grid(row=2, column=4)
        Insert_label1=Label(self.root,text="Insert Value 1(Date)").grid(row=0,column=0)
        self.Value1_Entry=Entry(self.root,bd=2,width=50,textvariable=self.DateValue.get())
        self.Value1_Entry.grid(row=0,column=1,sticky=W)

        Insert_label2=Label(self.root,text="Insert Value 2(NumberCode)").grid(row=1,column=0)
        self.Value2_Entry=Entry(self.root,bd=2,width=30,textvariable=self.NcodeValue.get())
        self.Value2_Entry.grid(row=1,column=1,sticky=W)
        Insert_label3=Label(self.root,text="Insert Value 3(Alphabet)").grid(row=2,column=0)
        self.Value3_Entry=Entry(self.root,bd=2,width=5,textvariable=self.CcodeValue.get())
        self.Value3_Entry.grid(row=2,column=1,sticky=W)

        Save_button=Button(self.root,text="Save",command=self.save_value_input).grid(row=3,column=4)

    def save_value_input(self):

            DateValue=self.Value1_Entry.get()
            NcodeValue=self.Value2_Entry.get()
            CcodeValue=self.Value3_Entry.get()



            #MsgER = messagebox.showerror("Insert Eror", "No Value , Please insert value")
            if (DateValue and  NcodeValue and CcodeValue)  :
                Msg = messagebox.askyesno("Save Value", "You want to save new value")
                if Msg == True:
                    Date_value = open('./Configure/Date_value.txt', "w")
                    Date_value.write(str(DateValue))
                    Date_value.close()
                    Number_value = open('./Configure/Number_value.txt', "w")
                    Number_value.write(str(NcodeValue))
                    Number_value.close()
                    Code_value = open('./Configure/Code_value.txt', "w")
                    Code_value.write(str(CcodeValue))
                    Code_value.close()
                    Ok_Next_button = Button(self.root, text="Ok and Next", command=self.page5_to_process).grid(row=3,column=5)
            else:
                #print(str(self.DateValue))
                MsgER=messagebox.showerror("Insert Eror","No Value , Please insert value")
    def page5_to_process(self):
        Msg = messagebox.askyesno("Next to Star", "You want to Start Process")
        if Msg == True:
            for ele in self.root.winfo_children():
                ele.destroy()
                #ele.quit()
            #self.root.destroy()
            if self.thread.isAlive() == True:
                print("thread Alive")
                #self.thread._Thread_stop()
                self.default_process_solution_1()

    def default_process_solution_1(self):
        for ele in self.root.winfo_children():
            ele.destroy()
            #ele.quit()

        self.panel = None
        self.panel2 = None
        self.panel3 = None
        self.panel4=None
        #self.root2 = tkinter.Tk()
        #self.root2.geometry('800x480')
        self.root.title("Solution 1 Process")
        self.ClickValue=10
        self.TextOcrRef()

        H=open('./Configure/AreaH.txt','r')
        self.HeightBbox=int(H.read())
        H.close()
        W = open('./Configure/AreaW.txt','r')
        self.WeightBbox =int(W.read())
        W.close()

        B_scale = open('./Configure/B_scale.txt', "r")
        self.var.set(int(B_scale.read()))
        B_scale.close()
        G_scale = open('./Configure/G_scale.txt', "r")
        self.var1.set(int(G_scale.read()))
        G_scale.close()
        R_scale = open('./Configure/R_scale.txt', "r")
        self.var2.set(int(R_scale.read()))
        R_scale.close()

        B_scale2 = open('./Configure/B_scale2.txt', "r")
        self.varMax.set(int(B_scale2.read()))
        B_scale2.close()
        G_scale2 = open('./Configure/G_scale2.txt', "r")
        self.varMax2.set(int(G_scale2.read()))
        G_scale2.close()
        R_scale2 = open('./Configure/R_scale2.txt', "r")
        self.varMax3.set(int(R_scale2.read()))
        R_scale2.close()
        R_scale2_min_for_Imgtocrop = open('./Configure/R_scale2_for_Imgtocrop.txt', "r")
        self.varMax4.set(int(R_scale2_min_for_Imgtocrop.read()))
        R_scale2_min_for_Imgtocrop.close()
        R_scale2_min_for_ImgWarp = open('./Configure/R_scale2_for_ImgWarp.txt', "r")
        self.varMax5.set(int(R_scale2_min_for_ImgWarp.read()))
        R_scale2_min_for_ImgWarp.close()

        Date_value = open('./Configure/Date_value.txt', "r")
        self.DateValue=str(Date_value.read())
        Date_value.close()
        Number_value = open('./Configure/Number_value.txt', "r")
        self.NcodeValue=str(Number_value.read())
        Number_value.close()
        Code_value = open('./Configure/Code_value.txt', "r")
        self.CcodeValue=str(Code_value.read())
        Code_value.close()

        rectY = open('./Configure/rectY.txt', 'r')
        self.rectY.set(int(rectY.read()))
        rectY.close()
        rectX = open('./Configure/rectX.txt', 'r')
        self.rectX.set(int(rectX.read()))
        rectX.close()
        sqY = open('./Configure/sqY.txt', 'r')
        self.sqY.set(int(sqY.read()))
        sqY.close()
        sqX = open('./Configure/sqX.txt', 'r')
        self.sqX.set(int(sqX.read()))
        sqX.close()

        rectY2 = open('./Configure/rectY2.txt', 'r')
        self.rectY2.set(int(rectY2.read()))
        rectY2.close()
        rectX2 = open('./Configure/rectX2.txt', 'r')
        self.rectX2.set(int(rectX2.read()))
        rectX2.close()
        sqY2 = open('./Configure/sqY2.txt', 'r')
        self.sqY2.set(int(sqY2.read()))
        sqY2.close()
        sqX2 = open('./Configure/sqX2.txt', 'r')
        self.sqX.set(int(sqX2.read()))
        sqX2.close()
        self.make_tempplate()
        if self.thread==None:
            self.thread=threading.Thread(target=self.videoLoop, args=())
            self.thread.daemon=True
            self.thread.start()

            #self.TextOCR()

            '''self.TextocrThread = threading.Thread(target=self.TextOCR, args=())
            self.TextocrThread.daemon = True
            self.TextocrThread.start()'''
        #self.root.destroy()
        #self.root.quit()self.thread.isAlive() == False or

    def page2_selectFile(self):
        for ele in self.root.winfo_children():
            ele.destroy()
        fileOpenButtun=Button(self.root,text="Open File",command=self.openDialog).grid(row=0,column=1)
        self.root.title("Select File")
        print(self.ClickValue)

    def videoLoop(self):
        self.ret, self.frame = self.vs.read()
        self.detectThread = threading.Thread(target=self.detect, args=())
        self.detectThread.daemon = True
        self.detectThread.start()

        try:
            while not self.stopEvent.is_set():
                self.ret,self.frame=self.vs.read()
                image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                self.frameShow=image
                if self.ClickValue==0 or self.ClickValue==10:

                    self.Show_panel01_0_0(self.frameShow)
        except RuntimeError as e:
            print("error runtime")
            self.vs.release()


    def scale(self):

        scale = Scale(self.root, from_=0, to=255, variable=self.var,label="B")
        scale.set(0)
        scale1 = Scale(self.root, from_=0, to=255, variable=self.var1,label="G")
        scale1.set(0)
        scale2 = Scale(self.root, from_=0, to=255, variable=self.var2,label="R")
        scale2.set(80)
        scale.grid(row=0,column=4,)
        scale1.grid(row=0,column=5)
        scale2.grid(row=0,column=6)
        '''scale2.pack(fill=BOTH, expand=0, side=RIGHT)
        scale1.pack(fill=BOTH, expand=0, side=RIGHT)
        scale.pack(fill=BOTH, expand=0, side=RIGHT)'''

    def scale2(self):

        scale = Scale(self.root, from_=0, to=255, variable=self.varMax)
        scale.set(255)
        scale1 = Scale(self.root, from_=0, to=255, variable=self.varMax2)
        scale1.set(255)
        scale2 = Scale(self.root, from_=0, to=255, variable=self.varMax3)
        scale2.set(255)
        scale3=Scale(self.root,from_=0, to=255,variable=self.varMax4,orient=tkinter.HORIZONTAL)
        scale3.set(90)
        scale4 = Scale(self.root, from_=0, to=255, variable=self.varMax5, orient=tkinter.HORIZONTAL)
        scale4.set(83)
        scale.grid(row=0, column=4)
        scale1.grid(row=0, column=5)
        scale2.grid(row=0, column=6)
        scale3.grid(row=0,column=7)
        scale4.grid(row=0,column=8)

    def scale3(self):
        #moregrap scale 20 10 18 10

        scale=Scale(self.root,from_=1,to=100,variable=self.rectY)
        scale.set(20)
        scale1=Scale(self.root,from_=1,to=100,variable=self.rectX)
        scale1.set(10)
        scale2=Scale(self.root,from_=1,to=100,variable=self.sqY)
        scale2.set(18)
        scale3=Scale(self.root,from_=1,to=100,variable=self.sqX)
        scale3.set(10)
        scale.grid(row=1, column=4)
        scale1.grid(row=1, column=5)
        scale2.grid(row=1, column=6)
        scale3.grid(row=1, column=7)
    def scale4(self):# use vssetting
        #moregrap scale 20 10 18 10
        self.rectY2=IntVar()
        self.rectX2=IntVar()
        self.sqY2=IntVar()
        self.sqX2=IntVar()
        scale=Scale(self.root,from_=1,to=100,variable=self.rectY2)
        scale.set(2)
        scale1=Scale(self.root,from_=1,to=100,variable=self.rectX2)
        scale1.set(62)
        scale2=Scale(self.root,from_=1,to=100,variable=self.sqY2)
        scale2.set(85)
        scale3=Scale(self.root,from_=1,to=100,variable=self.sqX2)
        scale3.set(2)
        scale.grid(row=2, column=4)
        scale1.grid(row=2, column=5)
        scale2.grid(row=2, column=6)
        scale3.grid(row=2, column=7)
    def detect(self):
        '''self.thread = threading.Thread(target=self.videoLoop, args=())
        self.thread.daemon = True
        self.thread.start()'''
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

                rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (self.rectY2.get(), self.rectX2.get()))
                try:

                    sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (self.sqY2.get(), self.sqX2.get()))
                except:
                    sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (34, 11))

                tophat = cv2.morphologyEx(thresh, cv2.MORPH_TOPHAT, rectKernel)
                np.seterr(divide='ignore', invalid='ignore')
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

                clone01 = np.dstack([thresh.copy()] * 3)
                self.treshImg=clone01

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


                pad = 30
                result = image[rect_min[0][1] - pad:rect_min[0][1] + rect_min[1][1] + pad,
                         rect_min[0][0] - pad:rect_min[0][0] + rect_min[1][0] + pad]
                h, w = result.shape[:2]
                if h <= 0 or w <= 0: #fixed box to tracking
                    result = image


                #print(result.shape[:2])
                if not self.HeightBbox is None or not  self.WeightBbox is None:
                    if self.HeightBbox >= h-40 and self.HeightBbox <= h+40:
                        if self.WeightBbox >= w-40 and self.WeightBbox <= w+40:
                            self.imgOrigin = result
                            self.Detect_flag=1
                        else:
                            self.Detect_flag=0

                            result = image
                    else:
                        #print("fu")
                        result = image
                        self.Detect_flag = 0


                if self.ClickValue==5:
                    h1, w1 = result.shape[:2]
                    self.Save_Bbox(h1,w1)
                    self.ClickValue=0

                self.imgOrigin=result
                self.ImgCap=result
                if self.ClickValue==0:
                    self.Show_panel02_0_1(self.treshImg)
                    self.Show_panel03_1_0(self.ImgCap)

                if self.ClickValue==10 and self.Detect_flag == 1 or self.ClickValue==2:
                    self.TextOCR2_no_loop()




    def onClose(self):
        cv2.imwrite("capture.png",self.imgOrigin)
        self.stopEvent.set()
        #self.vs.release()
        self.root.quit()
        #self.root.q
        #exit()
        #self.root.destroy()
    def make_tempplate(self):
        make01 = {}
        make02 = {}
        make03 = {}
        area01={}
        area02={}
        area03={}
        for idx, digi in enumerate(self.DateValue):
            if digi == '/' :
                make01[idx]= self.digits[10]
            else:
                for (i,img) in enumerate(self.digits):
                    if int(digi)==int(i):
                        make01[idx]=self.digits[i]

        area01 = np.hstack((make01[0],make01[1]))
        #area01 = np.hstack(make01[idx]) (57, 88)
       # area01 = PIL.Image.fromarray(make01)
        cv2.imshow("test",area01)
        print(make01)
        #area01 = PIL.Image.fromarray(area01)

        for idx,digi in enumerate(self.NcodeValue):
            if digi=='/':
                make02[idx]=self.digits[10]
            else:
                for i,img in enumerate(self.digits):
                    if int(digi)==int(i):
                        make02[idx]=img
        area02 = np.hstack(make02)
        for idx, digi in enumerate(self.CcodeValue):
            if digi == '/':
                make03[idx]=self.digits[10]
            elif digi == 'A':
                make03[idx] = self.digits[11]
            elif digi == 'B':
                make03[idx] = self.digits[12]
            elif digi == 'C':
                make03[idx] = self.digits[13]
            else:
                for i,img in enumerate(self.digits):
                    if int(digi) == int(i):
                        make03[idx] = img
        area03 = np.hstack(make03)


        #area02 = PIL.Image.fromarray(area02)
        #area03 = PIL.Image.fromarray(area03)
        '''area01.save('./TextRef/Area1.png')
        area02.save('./TextRef/Area2.png')
        area03.save('./TextRef/Area3.png')'''
        '''cv2.imwrite('./TextRef/Area1.png',area01)
        cv2.imwrite('./TextRef/Area2.png', area02)
        cv2.imwrite('./TextRef/Area3.png', area03)'''
    def TextOcrRef(self):
        ref=cv2.imread("./TextRef/temp.png",0)
        img=ref

        #config2 = r'--tessdata-dir "C:\\Program Files (x86)\\Tesseract-OCR\\tessdata "'

        ref = cv2.threshold(ref, 200, 255, cv2.THRESH_BINARY_INV)[1]
        #cv2.imshow('ref', ref)
        refCnt = cv2.findContours(ref.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        refCnt = refCnt[0] if imutils.is_cv2() else refCnt[1]
        refCnt = contours.sort_contours(refCnt, method="left-to-right")[0]
        self.digits = {}
        self.digits1={}
        self.digits2={}
        self.digits3={}
        self.roi = {}
        for (i, c) in enumerate(refCnt):
            (x, y, w, h) = cv2.boundingRect(c)
            x -= 5
            y -= 13
            w += 10
            h += 18
            self.roi[i] = ref[y:y + h, x:x + w]
            self.roi[i] = cv2.resize(self.roi[i], (57, 88))
            #cv2.imwrite("roi"+str(i)+'o.png',roi)
            self.digits[i] = self.roi[i]
        for idx in range(11):
            self.digits1[idx]=self.digits[idx]
        for idx in range(10):
            self.digits2[idx]=self.digits[idx]
        for idx in range(3):
            self.digits3[idx]=self.digits[11+idx]

        clone = np.dstack([ref.copy()] * 3)
        for c in refCnt:
            (x, y, w, h) = cv2.boundingRect(c)

            cv2.rectangle(clone, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # roi = ref[y:y + h, x:x + w]
        #cv2.imshow("Simple Method", clone)
        #cv2.imshow('roi', self.roi[8])
        #cv2.imshow("test",ref)
    def TextOCR(self):
        Noimg = cv2.imread('no_detect.png')
        while not self.stopEvent.is_set():
            if not self.imgOrigin is None:
                if self.Detect_flag==1 :
                    rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (self.rectY.get(), self.rectX.get()))
                    sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (self.sqY.get(), self.sqX.get()))
                    imgOrigin=self.imgOrigin
                    #imgOrigin = imutils.resize(imgOrigin, width=150)

                    gray = cv2.cvtColor(imgOrigin, cv2.COLOR_BGR2GRAY)
                    #tophat = cv2.morphologyEx(gray, cv2.MORPH_TOPHAT, rectKernel)
                    Imin = np.array([self.var.get(), self.var1.get(), self.varMax4.get()], dtype='uint8')
                    Imin2 = np.array([self.var.get(), self.var1.get(), self.varMax5.get()], dtype='uint8')
                    Imax = np.array([self.varMax.get(), self.varMax2.get(), self.varMax3.get()], dtype='uint8')
                    hsv = cv2.cvtColor(imgOrigin, cv2.COLOR_BGR2HSV)
                    masks = cv2.inRange(hsv, Imin, Imax)
                    masks2 = cv2.inRange(hsv, Imin2, Imax)
                    blurred = cv2.blur(masks, (1, 1))
                    blurred2 = cv2.blur(masks2, (1, 1))
                    img = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV)[1]
                    img2 = cv2.threshold(blurred2, 0, 255, cv2.THRESH_BINARY_INV)[1]
                    imgTocrop=img
                    imgWrap=img2

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
                    t2=thresh
                    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, sqKernel)
                    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                            cv2.CHAIN_APPROX_SIMPLE)
                    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
                    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

                    locs = []
                    tmpcnts = {}
                    clone01 = np.dstack([thresh.copy()] * 3)


                    font = cv2.FONT_HERSHEY_SIMPLEX
                    tmpcnts3 = {}
                    for (idx, c) in enumerate(cnts):
                        x, y, w, h = cv2.boundingRect(c)
                        x-=15
                        y-=8
                        w+=25
                        h+=10
                        #h=h+5
                        cv2.rectangle(clone01, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        tmpcnts[idx] = imgTocrop[y:y + h, x:x + w]
                        tmpcnts3[idx] = imgWrap[y:y + h, x:x + w]
                        #

                        locs.append((x, y, w, h))

                    locs = sorted(locs, key=lambda X: X[0])
                    #self.lock.acquire()
                    #self.Img.put(tmpcnts)
                    #self.lock.release()
                    #t = pytesseract.image_to_string(PIL.Image.fromarray(img), config=config, lang='eng')
                    #print(t)

                    img = clone01

                    if self.ClickValue==2:
                        self.Show_panel01_0_0(img)

                    output = []
                    kernel = np.ones((1, 1), np.uint8)
                    kernel2 = np.ones((2, 2), np.uint8)
                    kernel3 = np.ones((5, 5), np.uint8)
                    imgWrap2 = imgWrap




                    text = []
                    tmpcnts2 = {}
                    for i in range(len(tmpcnts)):
                        #text = []
                        try:
                            img=tmpcnts[i]
                            h, w = img.shape[:2]
                            img = imutils.resize(img, width=int(w / 2), height=int(h / 2))
                            img = tmpcnts[i]
                        except:
                            img=imgTocrop

                        tmpcnts2[i]=img
                        text.append(i)
                    if len(tmpcnts)==0:
                        self.Detect_flag=0 ##

                        tmpcnts2[0]=imgTocrop
                        tmpcnts3[0]=imgWrap

                    imgtest={}
                    imgtest2={}
                    charac = 0
                    for (i, (gX, gY, gW, gH)) in enumerate(locs):
                        groupOutput = []
                        img=tmpcnts2[i]

                        rectKernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 50))
                        sqKernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 50))
                        tophat2 = cv2.morphologyEx(img, cv2.MORPH_TOPHAT, rectKernel2)

                        np.seterr(divide='ignore', invalid='ignore')
                        gradX = cv2.Sobel(tophat2, ddepth=cv2.CV_64F, dx=0, dy=1, ksize=3)
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

                        try: digitCnts = contours.sort_contours(digitCnts,
                                                           method="left-to-right")[0]
                        except:
                            digitCnts = sorted(digitCnts, key=cv2.contourArea, reverse=True)
                        clone02 = np.dstack([thresh.copy()] * 3)
                        imgtest[i]=clone02

                        for c in digitCnts:

                            (x, y, w, h) = cv2.boundingRect(c)
                            x -= 3

                            w += 5

                            cv2.rectangle(clone02, (x, y), (x + w, y + h), (0, 255, 0), 2)
                            roi = tmpcnts3[i][y:y + h, x:x + w]
                            roi = cv2.morphologyEx(roi, cv2.MORPH_OPEN, kernel)
                            roi = cv2.morphologyEx(roi, cv2.MORPH_CLOSE, kernel)
                            roi = cv2.dilate(roi, kernel, iterations=1)
                            try:
                                roi = cv2.resize(roi, (57, 88))
                            except:
                                roi=cv2.resize(img, (57, 88))


                            imgtest2[charac]=roi
                            charac+=1

                            scores = []
                            DIGITS={}
                            if i==0:
                                DIGITS=self.digits1
                            elif i==1 :
                                DIGITS=self.digits2
                            elif i==2 :
                                DIGITS=self.digits3
                            else:
                                DIGITS=self.digits


                            for (digit, digitROI) in DIGITS.items():

                                result = cv2.matchTemplate(roi, digitROI,
                                                           cv2.TM_CCOEFF_NORMED)
                                (_, score, _, _) = cv2.minMaxLoc(result)

                                scores.append(score)

                            try:
                                if i==0:
                                    if str(np.argmax(scores))=='10':
                                        groupOutput.append('/')
                                    else:
                                        groupOutput.append(str(np.argmax(scores)))

                                elif i==2:
                                    if str(np.argmax(scores))=='0':
                                        groupOutput.append('A')
                                    elif str(np.argmax(scores))=='1':
                                        groupOutput.append('B')
                                    else:
                                        groupOutput.append('C')
                                else:

                                    groupOutput.append(str(np.argmax(scores)))
                            except:
                                    pass
                        gX += 15
                        gY += 8
                        gW -= 18
                        gH -= 10


                        output.append(groupOutput)
                        '''cv2.rectangle(imgWrap2, (gX - 5, gY - 5),
                                      (gX + gW + 5, gY + gH + 5), (255, 255, 255), 2)'''


                    img=img2
                    if self.ClickValue == 2:
                        self.Show_panel02_0_1(img)
                        self.Show_panel03_1_0(imgWrap)
                        try: self.Show_panel04_1_1(imgtest2[1])
                        except: pass
                    if self.ClickValue==10:
                        self.Show_panel01_0_0(self.frameShow)
                        self.Show_panel05_2_0(tmpcnts2[0])
                        self.Show_panel03_1_0(self.ImgCap)



                        try:
                            Label(self.root, text=output[0], width=20, font=("Helvetica", 20)).grid(row=0, column=1)
                            Label(self.root, text=output[1], width=20, font=("Helvetica", 20)).grid(row=1, column=1)
                            Label(self.root, text=output[2], width=20, font=("Helvetica", 20)).grid(row=2, column=1)
                            if self.DateValue== "".join(str(x) for x in output[0]):
                                #fg = "red"

                                Label(self.root, text="TRUE ", font=("Helvetica", 20),fg = "green").grid(row=0, column=2,sticky=W)
                            else:
                                Label(self.root, text="FAIL ", font=("Helvetica", 20), fg="red").grid(row=0, column=2,sticky=W)
                            if self.NcodeValue== "".join(str(x) for x in output[1]):
                                #fg = "red"
                                Label(self.root, text="TRUE ", font=("Helvetica", 20),fg = "green").grid(row=1, column=2,sticky=W)
                            else:
                                Label(self.root, text="FAIL ", font=("Helvetica", 20), fg="red").grid(row=1, column=2,sticky=W)
                            if str(self.CcodeValue)== "".join(str(x) for x in output[2]):
                                #fg = "red"
                                Label(self.root, text="TRUE ", font=("Helvetica", 20),fg = "green").grid(row=2, column=2,sticky=W)
                            else:
                                Label(self.root, text="FAIL ", font=("Helvetica", 20), fg="red").grid(row=2, column=2,sticky=W)
                        except:
                            pass

                else:
                    #img=cv2.imread('no_detect.png')
                    if self.ClickValue == 2:
                        self.Show_panel02_0_1(Noimg)
                        self.Show_panel03_1_0(Noimg)
                        self.Show_panel04_1_1(Noimg)
                    if self.ClickValue==10:
                        self.Show_panel01_0_0(self.frameShow)
                        self.Show_panel03_1_0(Noimg)
                        self.Show_panel05_2_0(Noimg)
                        Label(self.root, text="NONE", width=20, font=("Helvetica", 20)).grid(row=0, column=1)
                        Label(self.root, text="NONE", width=20, font=("Helvetica", 20)).grid(row=1, column=1)
                        Label(self.root, text="NONE", width=20, font=("Helvetica", 20)).grid(row=2, column=1)

    def TextOCR2_no_loop(self):
        Noimg = cv2.imread('no_detect.png')

        if not self.imgOrigin is None:
            if self.Detect_flag == 1:
                rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (self.rectY.get(), self.rectX.get()))
                sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (self.sqY.get(), self.sqX.get()))
                imgOrigin = self.imgOrigin
                # imgOrigin = imutils.resize(imgOrigin, width=150)

                gray = cv2.cvtColor(imgOrigin, cv2.COLOR_BGR2GRAY)
                # tophat = cv2.morphologyEx(gray, cv2.MORPH_TOPHAT, rectKernel)
                Imin = np.array([self.var.get(), self.var1.get(), self.varMax4.get()], dtype='uint8')
                Imin2 = np.array([self.var.get(), self.var1.get(), self.varMax5.get()], dtype='uint8')
                Imax = np.array([self.varMax.get(), self.varMax2.get(), self.varMax3.get()], dtype='uint8')
                hsv = cv2.cvtColor(imgOrigin, cv2.COLOR_BGR2HSV)
                masks = cv2.inRange(hsv, Imin, Imax)
                masks2 = cv2.inRange(hsv, Imin2, Imax)
                blurred = cv2.blur(masks, (1, 1))
                blurred2 = cv2.blur(masks2, (1, 1))
                img = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV)[1]
                img2 = cv2.threshold(blurred2, 0, 255, cv2.THRESH_BINARY_INV)[1]
                imgTocrop = img
                imgWrap = img2

                tophat = cv2.morphologyEx(img, cv2.MORPH_TOPHAT, rectKernel)
                img2 = img
                np.seterr(divide='ignore', invalid='ignore')
                gradX = cv2.Sobel(tophat, ddepth=cv2.CV_64F, dx=1, dy=0, ksize=7)
                gradX = np.absolute(gradX)
                (minVal, maxVal) = (np.min(gradX), np.max(gradX))
                gradX = (255 * ((gradX - minVal) / (maxVal - minVal)))
                gradX = gradX.astype("uint8")

                gradX = cv2.morphologyEx(gradX, cv2.MORPH_CLOSE, rectKernel)
                thresh = cv2.threshold(gradX, 0, 255,
                                       cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
                t2 = thresh
                thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, sqKernel)
                cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                        cv2.CHAIN_APPROX_SIMPLE)
                cnts = cnts[0] if imutils.is_cv2() else cnts[1]
                cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

                locs = []
                tmpcnts = {}
                clone01 = np.dstack([thresh.copy()] * 3)

                font = cv2.FONT_HERSHEY_SIMPLEX
                tmpcnts3 = {}
                for (idx, c) in enumerate(cnts):
                    x, y, w, h = cv2.boundingRect(c)
                    x -= 15
                    y -= 8
                    w += 25
                    h += 10
                    # h=h+5
                    cv2.rectangle(clone01, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    tmpcnts[idx] = imgTocrop[y:y + h, x:x + w]
                    tmpcnts3[idx] = imgWrap[y:y + h, x:x + w]
                    #

                    locs.append((x, y, w, h))

                locs = sorted(locs, key=lambda X: X[0])
                # self.lock.acquire()
                # self.Img.put(tmpcnts)
                # self.lock.release()
                # t = pytesseract.image_to_string(PIL.Image.fromarray(img), config=config, lang='eng')
                # print(t)

                img = clone01

                if self.ClickValue == 2:
                    self.Show_panel01_0_0(img)

                output = []
                kernel = np.ones((1, 1), np.uint8)
                kernel2 = np.ones((2, 2), np.uint8)
                kernel3 = np.ones((5, 5), np.uint8)
                imgWrap2 = imgWrap

                text = []
                tmpcnts2 = {}
                for i in range(len(tmpcnts)):
                    # text = []
                    try:
                        img = tmpcnts[i]
                        h, w = img.shape[:2]
                        img = imutils.resize(img, width=int(w / 2), height=int(h / 2))
                        img = tmpcnts[i]
                    except:
                        img = imgTocrop

                    tmpcnts2[i] = img
                    text.append(i)
                if len(tmpcnts) == 0:
                    self.Detect_flag = 0  ##

                    tmpcnts2[0] = imgTocrop
                    tmpcnts3[0] = imgWrap

                imgtest = {}
                imgtest2 = {}
                charac = 0
                for (i, (gX, gY, gW, gH)) in enumerate(locs):
                    groupOutput = []
                    img = tmpcnts2[i]

                    rectKernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 50))
                    sqKernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 50))
                    tophat2 = cv2.morphologyEx(img, cv2.MORPH_TOPHAT, rectKernel2)

                    np.seterr(divide='ignore', invalid='ignore')
                    gradX = cv2.Sobel(tophat2, ddepth=cv2.CV_64F, dx=0, dy=1, ksize=3)
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
                    imgtest[i] = clone02

                    for c in digitCnts:

                        (x, y, w, h) = cv2.boundingRect(c)
                        x -= 3

                        w += 5

                        cv2.rectangle(clone02, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        roi = tmpcnts3[i][y:y + h, x:x + w]
                        roi = cv2.morphologyEx(roi, cv2.MORPH_OPEN, kernel)
                        roi = cv2.morphologyEx(roi, cv2.MORPH_CLOSE, kernel)
                        roi = cv2.dilate(roi, kernel, iterations=1)
                        try:
                            roi = cv2.resize(roi, (57, 88))
                        except:
                            roi = cv2.resize(img, (57, 88))

                        imgtest2[charac] = roi
                        charac += 1

                        scores = []
                        DIGITS = {}
                        if i == 0:
                            DIGITS = self.digits1
                        elif i == 1:
                            DIGITS = self.digits2
                        elif i == 2:
                            DIGITS = self.digits3
                        else:
                            DIGITS = self.digits

                        for (digit, digitROI) in DIGITS.items():
                            result = cv2.matchTemplate(roi, digitROI,
                                                       cv2.TM_SQDIFF)
                            (_, score, _, _) = cv2.minMaxLoc(result)

                            scores.append(score)

                        try:
                            if i == 0:
                                if str(np.argmin(scores)) == '10':
                                    groupOutput.append('/')
                                else:
                                    groupOutput.append(str(np.argmin(scores)))

                            elif i == 2:
                                if str(np.argmin(scores)) == '0':
                                    groupOutput.append('A')
                                elif str(np.argmin(scores)) == '1':
                                    groupOutput.append('B')
                                else:
                                    groupOutput.append('C')
                            else:

                                groupOutput.append(str(np.argmin(scores)))
                        except:
                            pass
                    gX += 15
                    gY += 8
                    gW -= 18
                    gH -= 10

                    output.append(groupOutput)
                    '''cv2.rectangle(imgWrap2, (gX - 5, gY - 5),
                                  (gX + gW + 5, gY + gH + 5), (255, 255, 255), 2)'''

                img = img2
                if self.ClickValue == 2:
                    self.Show_panel02_0_1(img)
                    self.Show_panel03_1_0(imgWrap)
                    try:
                        self.Show_panel04_1_1(imgtest2[1])
                    except:
                        pass
                if self.ClickValue == 10:
                    #self.Show_panel01_0_0(self.frameShow)
                    self.Show_panel05_2_0(tmpcnts2[0])
                    self.Show_panel03_1_0(self.ImgCap)

                    try:
                        Label(self.root, text=output[0], width=20, font=("Helvetica", 20)).grid(row=0, column=1)
                        Label(self.root, text=output[1], width=20, font=("Helvetica", 20)).grid(row=1, column=1)
                        Label(self.root, text=output[2], width=20, font=("Helvetica", 20)).grid(row=2, column=1)
                        if self.DateValue == "".join(str(x) for x in output[0]):
                            # fg = "red"

                            Label(self.root, text="TRUE ", font=("Helvetica", 20), fg="green").grid(row=0, column=2,
                                                                                                    sticky=W)
                        else:
                            Label(self.root, text="FAIL ", font=("Helvetica", 20), fg="red").grid(row=0, column=2,
                                                                                                  sticky=W)
                        if self.NcodeValue == "".join(str(x) for x in output[1]):
                            # fg = "red"
                            Label(self.root, text="TRUE ", font=("Helvetica", 20), fg="green").grid(row=1, column=2,
                                                                                                    sticky=W)
                        else:
                            Label(self.root, text="FAIL ", font=("Helvetica", 20), fg="red").grid(row=1, column=2,
                                                                                                  sticky=W)
                        if str(self.CcodeValue) == "".join(str(x) for x in output[2]):
                            # fg = "red"
                            Label(self.root, text="TRUE ", font=("Helvetica", 20), fg="green").grid(row=2, column=2,
                                                                                                    sticky=W)
                        else:
                            Label(self.root, text="FAIL ", font=("Helvetica", 20), fg="red").grid(row=2, column=2,
                                                                                                  sticky=W)
                    except:
                        pass

            else:
                # img=cv2.imread('no_detect.png')
                if self.ClickValue == 2:
                    self.Show_panel02_0_1(Noimg)
                    self.Show_panel03_1_0(Noimg)
                    self.Show_panel04_1_1(Noimg)
                if self.ClickValue == 10:
                    #self.Show_panel01_0_0(self.frameShow)
                    self.Show_panel03_1_0(Noimg)
                    self.Show_panel05_2_0(Noimg)
                    Label(self.root, text="NONE", width=20, font=("Helvetica", 20)).grid(row=0, column=1)
                    Label(self.root, text="NONE", width=20, font=("Helvetica", 20)).grid(row=1, column=1)
                    Label(self.root, text="NONE", width=20, font=("Helvetica", 20)).grid(row=2, column=1)
def tesseract(idx,imgQ):
        img = imgQ.get()
        #l.acquire()

        config = (
            '-c tessedit_char_whitelist=0123456789ABC/ -c tessedit_char_blacklist=abcdefghijklmnopqrstuvwxyzDEFGHIJKLMNOPQRSTOUWXYZ\|-()*^><!$ -l eng --oem 1 --psm 7')
        #img = imgT[i]

                        #h, w = img.shape[:2]
                        #img = imutils.resize(img, width=int(w / 2), height=int(h / 2))
                #img = gray.get()
                #print("erore")
        t = pytesseract.image_to_string(PIL.Image.fromarray(img[idx]), config=config, lang='eng')
        #Txq.put(t)
        return t
                #print(t)
def multi_run_wrapper(args):
            return tesseract(*args)






if __name__ == '__main__':
    reciv,sendtoo=multiprocessing.Pipe()
    arr=multiprocessing.Array('i',range(10))
    TextQ = multiprocessing.Queue()
    ImgQ = multiprocessing.Queue(maxsize=3)
    t=App()
    t.root.mainloop()





