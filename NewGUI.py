import tkinter
import time
import os
import io
from tkinter import *
from tkinter import filedialog, messagebox

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


####enable when use picamera module
# from picamera.array import PiRGBArray
# from picamera import PiCamera
####enable when use picamera module
# import imu

class App():
    def __init__(self, ):
        #####disble when use videoloop_picamera
        self.vs = cv2.VideoCapture(0)
        #####
        self.root = tkinter.Tk()
        # self.scale()
        # self.scale2()
        self.Detect_flag = 0
        self.algorithm_flag = 1
        self.frameShow = None
        self.frame1 = None
        self.frame = None
        self.thread = None
        self.stopEvent = None

        #####disble when use videoloop_picamera
        self.ret, self.frameTemp = self.vs.read()
        #####
        self.Noimg = cv2.imread('no_detect.png')
        self.MultiOcr = None
        self.ClickValue = 0
        self.count_sum = 0
        self.pass_value=0
        self.fail_value=0

        self.pass_count=0
        self.fail_count=0
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
        self.treshImg = None
        self.ImgCap = None

        self.DateValue = StringVar()
        self.NcodeValue = StringVar()
        self.CcodeValue = StringVar()

        self.HeightBbox = None
        self.WeightBbox = None

        # self.box=queue.Queue()
        # self.cnts=queue.Queue()
        self.imgOrigin = None

        self.lock = multiprocessing.Lock()
        # self.TextOcrRef()
        self.panel = None
        self.panel2 = None
        self.panel3 = None
        self.panel4 = None
        self.panel5 = None
        self.panel6 = None  # not use
        self.buttom = None

        self.make01 = None
        self.make02 = None
        self.make03 = None
        self.area01 = None
        self.area02 = None
        self.area03 = None
        self.thresh = queue.Queue()
        self.result = queue.Queue()
        self.stopEvent = threading.Event()
        self.load_all_except_target()
        # self.load_all_value()

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

        # self.multi_OCR()
        # self.showThread=threading.Thread(target=self.show_panel,args=())
        # self.showThread.start()
        # self.scale()
        # self.TextOCR()

        self.root.wm_protocol("WM_DELETE_WINDOW", self.onClose)

    def Save_Bbox(self, h, w):
        self.HeightBbox = h
        self.WeightBbox = w

    def Click_ValueBbox(self):
        self.ClickValue = 5
        print(5)

    def settingButton(self):
        # self.ClickValue+=1
        self.page2_selectFile()

    def page1_selectOption(self):
        self.root.geometry('800x480')
        self.root.title("Start page")
        Button(self.root, text='Default', command=self.default_process_solution_1).grid(row=1, column=1, columnspan=2,
                                                                                        rowspan=2, sticky=W + N + E + S)
        Button(self.root, text='Setting', command=self.settingButton).grid(row=1, column=3, columnspan=2, rowspan=2,
                                                                           sticky=W + N + E + S)

    def openDialog(self):
        self.filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                                   filetypes=(("*png files", "*.png"), ("*jpg files", "*.jpg")))
        self.importImg()

    def Show_panel01_0_0(self, img):
        try:
            img = imutils.resize(img, width=150, height=100)
        except:
            img = img
        img = PIL.Image.fromarray(img)
        img = PIL.ImageTk.PhotoImage(img)
        if self.panel is None:
            self.panel = tkinter.Label(image=img, width=160, height=120)
            self.panel.image = img
            self.panel.grid(row=0, column=0)
        else:
            self.panel.configure(image=img)
            self.panel.image = img

    def Show_panel02_0_1(self, img):
        try:
            img = imutils.resize(img, width=150, height=100)
        except:
            img = img
        img = PIL.Image.fromarray(img)
        img = PIL.ImageTk.PhotoImage(img)
        if self.panel2 is None:
            self.panel2 = tkinter.Label(image=img, width=160, height=120)
            self.panel2.image = img
            self.panel2.grid(row=0, column=1)
        else:
            self.panel2.configure(image=img)
            self.panel2.image = img

    def Show_panel03_1_0(self, img):
        try:
            img = imutils.resize(img, width=150, height=100)
        except:
            img = img
        img = PIL.Image.fromarray(img)
        img = PIL.ImageTk.PhotoImage(img)
        if self.panel3 is None:
            self.panel3 = tkinter.Label(image=img, width=160, height=120)
            self.panel3.image = img
            self.panel3.grid(row=1, column=0)
        else:
            self.panel3.configure(image=img)
            self.panel3.image = img

    def Show_panel04_1_1(self, img):
        try:
            img = imutils.resize(img, width=150, height=100)
        except:
            img = img
        img = PIL.Image.fromarray(img)
        img = PIL.ImageTk.PhotoImage(img)
        if self.panel4 is None:
            self.panel4 = tkinter.Label(image=img, width=160, height=120)
            self.panel4.image = img

            self.panel4.grid(row=1, column=1)
        else:
            self.panel4.configure(image=img)
            self.panel4.image = img

    def Show_panel05_2_0(self, img):
        try:
            img = imutils.resize(img, width=150, height=100)
        except:
            img = img
        img = PIL.Image.fromarray(img)
        img = PIL.ImageTk.PhotoImage(img)
        if self.panel5 is None:
            self.panel5 = tkinter.Label(image=img, width=160, height=120)
            self.panel5.image = img
            self.panel5.grid(row=2, column=0)
        else:
            self.panel5.configure(image=img)
            self.panel5.image = img
    def Show_panel06_3_0(self, img):
        try:
            img = imutils.resize(img, width=150, height=100)
        except:
            img = img
        img = PIL.Image.fromarray(img)
        img = PIL.ImageTk.PhotoImage(img)
        if self.panel6 is None:
            self.panel6 = tkinter.Label(image=img)###fix w,h
            self.panel6.image = img
            self.panel6.grid(row=3, column=0)
        else:
            self.panel6.configure(image=img)
            self.panel6.image = img
    def importImg(self):
        # img=PIL.Image.open(self.filename)
        MegLabel = StringVar()

        img = cv2.imread(self.filename)

        try:
            img2 = img
            self.Show_panel01_0_0(img)
        except:
            self.panel = None
            Nonelabel = Label(self.root, text="<<<<None Image Choose file(agian) Please>>>").grid(row=0, column=0)

        if self.panel is None:

            Nonelabel = Label(self.root, textvariable=MegLabel).grid(row=1, column=1)
            MegLabel.set("None")
        else:
            fileImportButton = Button(self.root, text="Import", command=lambda: self.Save_tempImg(img2)).grid(row=0,
                                                                                                              column=2)
            MegLabel.set("Get Image")
            # Nonelabel.destroy()
            Getlabel = Label(self.root, textvariable=MegLabel).grid(row=1, column=1)

    def Save_tempImg(self, img):
        error = 0
        Msg = messagebox.askyesno("Import and Install ROI", "Do you want to Import and install ROI")
        if Msg == True:
            if img is None:
                NoImportLabel = Label(self.root, text="You do not import Image and install ROI(use default)").grid(
                    row=1, column=1)
            else:
                cv2.imwrite('./TextRef/temp.png', img=img)  # chang to temp.png
            try:
                self.TextOcrRef()
                error = 0
            except:
                messagebox.showerror(title="File Error", message="File Error Import new file")
                error = 1

        else:
            NoImportLabel = Label(self.root, text="You do not import Image and install ROI(use default)").grid(row=1,
                                                                                                               column=1)
            self.TextOcrRef()
        if error == 0:
            OkNextButton = Button(self.root, text="OK and Next", command=self.page3_setting_vscap).grid(row=2, column=2)

    def reset_bbox(self):
        self.HeightBbox = None
        self.WeightBbox = None

    def page3_setting_vscap(self):
        self.panel = None
        for ele in self.root.winfo_children():
            ele.destroy()
        self.root.title("Setting Video Capture")
        self.scale()
        self.scale4()
        self.thread = threading.Thread(target=self.videoLoop, args=())
        self.thread.daemon = True
        self.thread.start()

        BboxSaveButton = Button(self.root, text="Target Area", command=self.Click_ValueBbox).grid(row=1, column=2)
        ResetBboxSaveButton = Button(self.root, text="Reset", command=self.reset_bbox).grid(row=2, column=2)
        OkNextButton = Button(self.root, text="OK and Next", command=self.page3_To_page4).grid(row=3, column=3)

    def page3_To_page4(self):
        self.ClickValue = 5
        Msg = messagebox.askyesno("Save and Next", "Save target Area and Other setting")
        if Msg == True:
            self.ClickValue = 2
            self.panel = None
            Area_configre_H = open('./Configure/AreaH.txt', "w")
            Area_configre_H.write(str(self.HeightBbox))
            Area_configre_H.close()
            Area_configre_W = open('./Configure/AreaW.txt', "w")
            Area_configre_W.write(str(self.WeightBbox))
            Area_configre_W.close()
            B_scale = open('./Configure/B_scale.txt', "w")
            B_scale.write(str(self.var.get()))
            B_scale.close()
            G_scale = open('./Configure/G_scale.txt', "w")
            G_scale.write(str(self.var1.get()))
            G_scale.close()
            R_scale = open('./Configure/R_scale.txt', "w")
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
            self.ClickValue = 2
            self.page4_settingDigit()

    def page4_settingDigit(self):
        self.ClickValue = 2
        for ele in self.root.winfo_children():
            ele.destroy()
        self.panel = None
        self.panel2 = None
        self.panel3 = None
        if self.thread.isAlive() == True:
            print("thread Alive")
            self.scale2()
            self.scale3()
            # self.scale4()
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
            G_scale2 = open('./Configure/G_scale2.txt', "w")
            G_scale2.write(str(self.varMax2.get()))
            G_scale2.close()
            R_scale2 = open('./Configure/R_scale2.txt', "w")
            R_scale2.write(str(self.varMax3.get()))
            R_scale2.close()
            R_scale2_min_for_Imgtocrop = open('./Configure/R_scale2_for_Imgtocrop.txt', "w")
            R_scale2_min_for_Imgtocrop.write(str(self.varMax4.get()))
            R_scale2_min_for_Imgtocrop.close()
            R_scale2_min_for_ImgWarp = open('./Configure/R_scale2_for_ImgWarp.txt', "w")
            R_scale2_min_for_ImgWarp.write(str(self.varMax5.get()))
            R_scale2_min_for_ImgWarp.close()
            '''self.rectY = IntVar()
            self.rectX = IntVar()
            self.sqY = IntVar()
            self.sqX = IntVar()'''
            rectY = open('./Configure/rectY.txt', 'w')
            rectY.write(str(self.rectY.get()))
            rectY.close()
            rectX = open('./Configure/rectX.txt', 'w')
            rectX.write(str(self.rectX.get()))
            rectX.close()
            sqY = open('./Configure/sqY.txt', 'w')
            sqY.write(str(self.sqY.get()))
            sqY.close()
            sqX = open('./Configure/sqX.txt', 'w')
            sqX.write(str(self.sqX.get()))
            sqX.close()
            self.ClickValue = 3
            self.page5_Insert_Value()

    def load_default_value(self):
        Date_value = open('./Configure/Date_value.txt', "r")

        self.Value1_Entry.insert(END, str(Date_value.read()))
        Date_value.close()
        Number_value = open('./Configure/Number_value.txt', "r")
        self.Value2_Entry.insert(END, str(Number_value.read()))
        Number_value.close()
        Code_value = open('./Configure/Code_value.txt', "r")
        self.Value3_Entry.insert(END, str(Code_value.read()))
        Code_value.close()

    def page5_Insert_Value(self):
        self.ClickValue = 3
        self.root.title("Insert Value")

        self.ClickValue = 3

        for ele in self.root.winfo_children():
            ele.destroy()
        self.panel = None
        self.panel2 = None
        self.panel3 = None
        self.panel4 = None
        Button(self.root, text="Default load", command=self.load_default_value).grid(row=2, column=4)
        Insert_label1 = Label(self.root, text="Insert Value 1(Date)").grid(row=0, column=0)
        self.Value1_Entry = Entry(self.root, bd=2, width=50, textvariable=self.DateValue)
        self.Value1_Entry.grid(row=0, column=1, sticky=W)

        Insert_label2 = Label(self.root, text="Insert Value 2(NumberCode)").grid(row=1, column=0)
        self.Value2_Entry = Entry(self.root, bd=2, width=30, textvariable=self.NcodeValue)
        self.Value2_Entry.grid(row=1, column=1, sticky=W)
        Insert_label3 = Label(self.root, text="Insert Value 3(Alphabet)").grid(row=2, column=0)
        self.Value3_Entry = Entry(self.root, bd=2, width=5, textvariable=self.CcodeValue)
        self.Value3_Entry.grid(row=2, column=1, sticky=W)

        Save_button = Button(self.root, text="Save", command=self.save_value_input).grid(row=3, column=4)

    def save_value_input(self):

        DateValue = self.Value1_Entry.get()
        NcodeValue = self.Value2_Entry.get()
        CcodeValue = self.Value3_Entry.get()

        # MsgER = messagebox.showerror("Insert Eror", "No Value , Please insert value")
        if (DateValue and NcodeValue and CcodeValue):
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
                Ok_Next_button = Button(self.root, text="Ok and Next", command=self.page5_to_process).grid(row=3,
                                                                                                           column=5)
        else:
            # print(str(self.DateValue))
            MsgER = messagebox.showerror("Insert Eror", "No Value , Please insert value")

    def page5_to_process(self):
        Msg = messagebox.askyesno("Next to Star", "You want to Start Process")
        if Msg == True:
            for ele in self.root.winfo_children():
                ele.destroy()
                # ele.quit()
            # self.root.destroy()
            if self.thread.isAlive() == True:
                print("thread Alive")
                # self.thread._Thread_stop()
                self.default_process_solution_1()

    def default_process_solution_1(self):
        for ele in self.root.winfo_children():
            ele.destroy()
            # ele.quit()

        self.panel = None
        self.panel2 = None
        self.panel3 = None
        self.panel4 = None
        # self.root2 = tkinter.Tk()
        # self.root2.geometry('800x480')
        self.root.title("Solution 1 Process")
        self.ClickValue = 10
        self.TextOcrRef()
        self.load_all_value()

        self.make_tempplate()
        Button(self.root, text="Algorithm 1", command=self.add_algorithm1_flag).grid(row=0, column=4)
        Button(self.root, text="Algorithm 2", command=self.add_algorithm2_flag).grid(row=1, column=4)
        Button(self.root, text="Algorithm 3", command=self.add_algorithm3_flag).grid(row=2, column=4)

        if self.thread == None:
            self.thread = threading.Thread(target=self.videoLoop, args=())
            self.thread.daemon = True
            self.thread.start()

            # self.TextOCR()

            '''self.TextocrThread = threading.Thread(target=self.TextOCR, args=())
            self.TextocrThread.daemon = True
            self.TextocrThread.start()'''
        # self.root.destroy()
        # self.root.quit()self.thread.isAlive() == False or

    def add_algorithm1_flag(self):
        self.algorithm_flag = 1

    def add_algorithm2_flag(self):
        self.algorithm_flag = 2

    def add_algorithm3_flag(self):
        self.algorithm_flag = 3

    def load_all_value(self):
        H = open('./Configure/AreaH.txt', 'r')
        self.HeightBbox = int(H.read())
        H.close()
        W = open('./Configure/AreaW.txt', 'r')
        self.WeightBbox = int(W.read())
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
        self.DateValue = str(Date_value.read())
        Date_value.close()
        Number_value = open('./Configure/Number_value.txt', "r")
        self.NcodeValue = str(Number_value.read())
        Number_value.close()
        Code_value = open('./Configure/Code_value.txt', "r")
        self.CcodeValue = str(Code_value.read())
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

    def load_all_except_target(self):
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
        self.DateValue = str(Date_value.read())
        Date_value.close()
        Number_value = open('./Configure/Number_value.txt', "r")
        self.NcodeValue = str(Number_value.read())
        Number_value.close()
        Code_value = open('./Configure/Code_value.txt', "r")
        self.CcodeValue = str(Code_value.read())
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

    def page2_selectFile(self):
        for ele in self.root.winfo_children():
            ele.destroy()
        fileOpenButtun = Button(self.root, text="Open File", command=self.openDialog).grid(row=0, column=1)
        defauil_bnt = Button(self.root, text="Use default", command=self.page2_default_selection).grid(row=0, column=2)
        self.root.title("Select File")
        print(self.ClickValue)

    def page2_default_selection(self):
        self.TextOcrRef()
        self.page3_setting_vscap()

    def videoLoop(self):

        self.ret, self.frame = self.vs.read()  # temp for fix
        self.start_thread_detect()
        # self.detectThread.join()
        # self.detect()
        try:
            while not self.stopEvent.is_set():

                self.ret, self.frame = self.vs.read()

                # self.detectThread.run()
                image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                self.frameShow = image
                if self.ClickValue == 0 or self.ClickValue == 10:
                    self.Show_panel01_0_0(self.frameShow)
        except RuntimeError as e:
            print("error runtime")
            self.vs.release()

    def start_thread_detect(self):
        self.detectThread = threading.Thread(target=self.detect, args=())

        self.detectThread.daemon = True
        self.detectThread.start()

    def videoLoop_picamera(self):
        self.frame_temp()
        camera = PiCamera()
        camera.resolution = (640, 480)
        camera.framerate = 60
        camera.rotation = 180
        rawCapture = PiRGBArray(camera, size=(640, 480))

        # time.sleep(0.1)
        stream = camera.capture_continuous(rawCapture, format="bgr", use_video_port=True)

        # self.frame=f2.array
        # self.frame=stream[0].array

        self.detectThread = threading.Thread(target=self.detect, args=())
        self.detectThread.daemon = True
        self.detectThread.start()
        try:
            while not self.stopEvent.is_set():

                for (i, f) in enumerate(stream):
                    self.frame = f.array
                    image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)

                    self.frameShow = image
                    if self.ClickValue == 0 or self.ClickValue == 10:
                        self.Show_panel01_0_0(self.frameShow)
                    rawCapture.truncate(0)

        except RuntimeError:
            print("error runtime")

        stream.close()
        rawCapture.close()
        camera.close()

    def frame_temp(self):  # frame temp when use videoloop_picamera
        camera = PiCamera()
        camera.resolution = (640, 480)
        camera.framerate = 30
        camera.rotation = 180
        rawCapture = PiRGBArray(camera, size=(640, 480))

        time.sleep(0.1)
        stream = camera.capture_continuous(rawCapture, format="bgr", use_video_port=True)
        for (i, f) in enumerate(stream):
            self.frame = np.asarray(f.array)
            break
        stream.close()
        rawCapture.close()
        camera.close()

    def scale(self):

        scale = Scale(self.root, from_=0, to=255, variable=self.var, label="B")
        scale.set(self.var.get())
        scale1 = Scale(self.root, from_=0, to=255, variable=self.var1, label="G")
        scale1.set(self.var1.get())
        scale2 = Scale(self.root, from_=0, to=255, variable=self.var2, label="R")
        scale2.set(self.var2.get())
        scale.grid(row=0, column=4, )
        scale1.grid(row=0, column=5)
        scale2.grid(row=0, column=6)
        '''scale2.pack(fill=BOTH, expand=0, side=RIGHT)
        scale1.pack(fill=BOTH, expand=0, side=RIGHT)
        scale.pack(fill=BOTH, expand=0, side=RIGHT)'''

    def scale2(self):

        scale = Scale(self.root, from_=0, to=255, variable=self.varMax)
        scale.set(self.varMax.get())
        scale1 = Scale(self.root, from_=0, to=255, variable=self.varMax2)
        scale1.set(self.varMax2.get())
        scale2 = Scale(self.root, from_=0, to=255, variable=self.varMax3)
        scale2.set(self.varMax3.get())
        scale3 = Scale(self.root, from_=0, to=255, variable=self.varMax4, orient=tkinter.HORIZONTAL)
        scale3.set(self.varMax4.get())
        scale4 = Scale(self.root, from_=0, to=255, variable=self.varMax5, orient=tkinter.HORIZONTAL)
        scale4.set(self.varMax5.get())
        scale.grid(row=0, column=4)
        scale1.grid(row=0, column=5)
        scale2.grid(row=0, column=6)
        scale3.grid(row=0, column=7)
        scale4.grid(row=0, column=8)

    def scale3(self):
        # moregrap scale 20 10 18 10

        scale = Scale(self.root, from_=1, to=100, variable=self.rectY)
        scale.set(self.rectY.get())
        scale1 = Scale(self.root, from_=1, to=100, variable=self.rectX)
        scale1.set(self.rectX.get())
        scale2 = Scale(self.root, from_=1, to=100, variable=self.sqY)
        scale2.set(self.sqY.get())
        scale3 = Scale(self.root, from_=1, to=100, variable=self.sqX)
        scale3.set(self.sqX.get())
        scale.grid(row=1, column=4)
        scale1.grid(row=1, column=5)
        scale2.grid(row=1, column=6)
        scale3.grid(row=1, column=7)

    def scale4(self):  # use vssetting
        # moregrap scale 20 10 18 10

        scale = Scale(self.root, from_=1, to=100, variable=self.rectY2)
        scale.set(self.rectY2.get())
        scale1 = Scale(self.root, from_=1, to=100, variable=self.rectX2)
        scale1.set(self.rectX2.get())
        scale2 = Scale(self.root, from_=1, to=100, variable=self.sqY2)
        scale2.set(self.sqY2.get())
        scale3 = Scale(self.root, from_=1, to=100, variable=self.sqX2)
        scale3.set(self.sqX2.get())
        scale.grid(row=2, column=4)
        scale1.grid(row=2, column=5)
        scale2.grid(row=2, column=6)
        scale3.grid(row=2, column=7)

    def detect(self):
        '''self.thread = threading.Thread(target=self.videoLoop, args=())
        self.thread.daemon = True
        self.thread.start()'''

        self.make_tempplate()
        while not self.stopEvent.is_set():
            # ret,img= self.vs.read()
            # img=self.frame
            start_time = time.time()
            result, image = self.calculate_detect()
            # result, image = self.calculate_detect_multithread()

            h, w = result.shape[:2]

            if h <= 0 or w <= 0:  # fixed box to tracking
                result = image

            # M = cv2.getPerspectiveTransform(np.float32(screenCnt), np.float32(box3))
            # result = cv2.warpPerspective(result, M, (h, w))
            # print(result.shape[:2])
            # result = self.check_target_area(result, image, h, w)
            self.imgOrigin = result
            if self.ClickValue == 5:
                h1, w1 = result.shape[:2]
                self.Save_Bbox(h1, w1)
                self.ClickValue = 0
            else:
                pass
            self.imgOrigin = result
            self.ImgCap = result
            if self.ClickValue == 0:
                self.Show_panel02_0_1(self.treshImg)
                self.Show_panel03_1_0(self.ImgCap)
            else:
                pass
            if self.ClickValue == 10 and self.Detect_flag == 1 or self.ClickValue == 2:
                # self.TextOCR2_no_loop()
                # self.ocr_thread()
                ocrthread = threading.Thread(target=self.TextOCR2_no_loop, args=())
                ocrthread.daemon = True
                ocrthread.run()

            else:
                self.no_detect()
            if self.ClickValue == 10:
                sum_string = "Total :"+str(self.count_sum)
                Label(self.root, text=sum_string, font=("Helvetica", 16)).grid(row=3, column=2)
                pass_string="Pass :"+str(self.pass_count)
                Label(self.root, text=pass_string, font=("Helvetica", 16), fg="green").grid(row=3, column=3)
                fail_string="Fail :"+str(self.fail_count)
                Label(self.root, text=fail_string, font=("Helvetica", 16), fg="red").grid(row=3, column=4)
                #self.sum_state.update()

            # print(threading.enumerate())
            print("--- %s seconds ---" % (time.time() - start_time))

    def calculate_detect_multithread(self):
        pool = ThreadPool(processes=5)

        async_result = pool.apply_async(self.calculate_detect, )  # tuple of args for foo
        pool.close()

        pool.join()
        # do some other stuff in the main process

        return_val = async_result.get()
        return return_val

    def calculate_detect(self):

        # self.ret, self.frame = self.vs.read()##change or disble when use picamera

        image = self.frame
        orig = image.copy()
        ratio = image.shape[0] / 300.0
        image = imutils.resize(image, height=300)
        # chang resolution for fix
        image_center = (image.shape[0] / 2, image.shape[1] / 2)

        Imin = np.array([self.var.get(), self.var1.get(), self.var2.get()], dtype='uint8')
        Imax = np.array([255, 255, 255], dtype='uint8')
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        masks = cv2.inRange(hsv, Imin, Imax)
        blurred = cv2.blur(masks, (5, 5))

        (_, thresh) = cv2.threshold(blurred, 180, 255, cv2.THRESH_BINARY_INV)

        rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (self.rectY2.get(), self.rectX2.get()))
        try:

            sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (self.sqY2.get(), self.sqX2.get()))
        except cv2.error as e:
            # print("error"+str(e))
            sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (34, 11))

        tophat = cv2.morphologyEx(thresh, cv2.MORPH_TOPHAT, rectKernel)
        np.seterr(divide='ignore', invalid='ignore')
        gradX = cv2.Sobel(tophat, ddepth=cv2.CV_32F, dx=1, dy=0,
                          ksize=7)
        gradX = np.absolute(gradX)
        (minVal, maxVal) = (np.min(gradX), np.max(gradX))
        gradX = (255 * ((gradX - minVal) / (maxVal - minVal)))
        gradX = gradX.astype("uint8")

        gradX = cv2.morphologyEx(gradX, cv2.MORPH_CLOSE, rectKernel)
        thresh = cv2.threshold(gradX, 0, 255,
                               cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, sqKernel)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
        closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

        kernelp = np.ones((15, 15), np.uint8)
        closed = cv2.erode(closed, None, iterations=4)
        closed = cv2.dilate(closed, kernelp, iterations=5)

        _, cnts, hierarchy = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # _, cnts2, hierarchy2 = cv2.findContours(gradient.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # c2 = sorted(cnts2, key=cv2.contourArea, reverse=True)[0]

        clone01 = np.dstack([closed.copy()] * 3)
        self.treshImg = clone01
        # rect2 = cv2.minAreaRect(c2)
        # box2 = cv2.boxPoints(rect2)
        # box2 = np.int0(box2)
        if len(cnts) == 0:
            cnts = np.float32([[[0, 0], [400, 0], [0, 300], [400, 400]]])
        else:
            pass
        c = sorted(cnts, key=cv2.contourArea, reverse=True)[0]
        # self.cnt_area_check(c)
        rect = cv2.minAreaRect(c)
        box = cv2.boxPoints(rect)

        box = np.int0(box)
        # res = cv2.bitwise_and(image, image, mask=closed)

        box3 = box

        d_min = 500
        rect_min = [[0, 0], [0, 0]]
        rect3 = cv2.boundingRect(box3)
        pt1 = (rect3[0], rect3[1])
        c = (rect3[0] + rect3[2] * 1 / 2, rect3[1] + rect3[3] * 1 / 2)
        d = np.sqrt((c[0] - image_center[0]) ** 2 + (c[1] - image_center[1]) ** 2)
        screenCnt = None
        if d < d_min:
            d_min = d
            rect_min = [pt1, (rect3[2], rect3[3])]
            # screenCnt=[]
            cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

            for c in cnts:
                # approximate the contour

                self.cnt_area_check(c)
                peri = cv2.arcLength(c, True)
                approx = cv2.approxPolyDP(c, 0.02 * peri, True)

                # if our approximated contour has four points, then we
                # can assume that we have found our screen
                if len(approx) == 4:
                    screenCnt = approx
                    break
                else:
                    pass
        else:
            pass
        # screenCnt[1]=screenCnt[1]+20
        if screenCnt is None:
            screenCnt = np.float32([[0, 0], [300, 0], [0, 300], [300, 300]])
            pts = screenCnt.reshape(4, 2)
        else:
            pts = screenCnt.reshape(4, 2)

        if self.ClickValue == 10:
            if self.Detect_flag == 0:
                result = image
            elif self.Detect_flag == 1:
                result = perspactive_transform(orig, pts, ratio)
                # result=pool_perspective(orig,pts,ratio,2)

        else:
            result = perspactive_transform(orig, pts, ratio)
            # result = pool_perspective(orig, pts, ratio, 2)
        # result = pool_perspective(orig, pts, ratio, 2)
        return result, image

    def cnt_area_check(self, c):
        x, y, w, h = cv2.boundingRect(c)
        # print(str(w)+" "+str(h))
        if self.ClickValue == 5:
            # h1, w1 = result.shape[:2]
            self.Save_Bbox(h, w)
            self.ClickValue = 0
        if not self.HeightBbox is None or not self.WeightBbox is None:
            if h - 20 <= self.HeightBbox <= h + 30:
                if w - 20 <= self.WeightBbox <= w + 30:
                    self.Detect_flag = 1
                else:
                    if self.Detect_flag == 1:
                        #self.count_sum += 1
                        self.change_state()

                    self.Detect_flag = 0
            else:
                if self.Detect_flag == 1:
                    #self.count_sum += 1
                    self.change_state()
                self.Detect_flag = 0
        else:
            pass
    def change_state(self):
        self.count_sum += 1
        if self.pass_value==1:
            self.pass_count+=1
        else:
            self.fail_count+=1
        self.pass_value = 0
        self.fail_value = 0
    def check_target_area(self, result, image, h, w):

        if not self.HeightBbox is None or not self.WeightBbox is None:
            if h - 40 <= self.HeightBbox <= h + 40:
                if w - 40 <= self.WeightBbox <= w + 40:
                    self.imgOrigin = result
                    self.Detect_flag = 1
                else:
                    self.Detect_flag = 0

                    result = image
            else:
                # print("fu")
                result = image
                self.Detect_flag = 0
        else:
            pass
        return result

    def onClose(self):
        cv2.imwrite("capture.png", self.imgOrigin)
        self.stopEvent.set()
        # self.vs.release()
        self.root.quit()
        # self.root.q
        # exit()
        # self.root.destroy()

    def make_tempplate(self):
        make01 = {}
        make02 = {}
        make03 = {}

        for idx, digi in enumerate(self.DateValue):
            if digi == '/':
                make01[idx] = self.digits[10]
            else:
                for (i, img) in enumerate(self.digits):
                    if int(digi) == int(i):
                        make01[idx] = self.digits[i]

        area01 = np.hstack((np.asarray(img) for (ik, img) in make01.items()))

        for idx, digi in enumerate(self.NcodeValue):
            if digi == '/':
                make02[idx] = self.digits[10]
            else:
                for i, img in enumerate(self.digits):
                    if int(digi) == int(i):
                        make02[idx] = self.digits[i]

        area02 = np.hstack((np.asarray(img) for (ik, img) in make02.items()))

        for idx, digi in enumerate(self.CcodeValue):
            if digi == '/':
                make03[idx] = self.digits[10]
            elif digi == 'A':
                make03[idx] = self.digits[11]
            elif digi == 'B':
                make03[idx] = self.digits[12]
            elif digi == 'C':
                make03[idx] = self.digits[13]
            else:
                for i, img in enumerate(self.digits):
                    if int(digi) == int(i):
                        make03[idx] = self.digits[i]
        area03 = np.hstack((np.asarray(img) for (ik, img) in make03.items()))

        # area02 = PIL.Image.fromarray(area02)
        # area03 = PIL.Image.fromarray(area03)
        '''area01.save('./TextRef/Area1.png')
        area02.save('./TextRef/Area2.png')
        area03.save('./TextRef/Area3.png')'''
        self.area01 = area01
        self.area02 = area02
        self.area03 = area03
        self.make01 = make01
        self.make02 = make02
        self.make03 = make03
        cv2.imwrite('./TextRef/Area1.png', area01)
        cv2.imwrite('./TextRef/Area2.png', area02)
        cv2.imwrite('./TextRef/Area3.png', area03)

    def TextOcrRef(self):
        ref = cv2.imread("./TextRef/temp.png", 0)
        img = ref

        # config2 = r'--tessdata-dir "C:\\Program Files (x86)\\Tesseract-OCR\\tessdata "'

        ref = cv2.threshold(ref, 200, 255, cv2.THRESH_BINARY_INV)[1]
        # cv2.imshow('ref', ref)
        refCnt = cv2.findContours(ref.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        refCnt = refCnt[0] if imutils.is_cv2() else refCnt[1]
        refCnt = contours.sort_contours(refCnt, method="left-to-right")[0]
        self.digits = {}
        self.digits1 = {}
        self.digits2 = {}
        self.digits3 = {}
        self.roi = {}
        for (i, c) in enumerate(refCnt):
            (x, y, w, h) = cv2.boundingRect(c)
            ######PAD
            x -= 4
            y -= 8
            w += 8
            h += 13
            #######PAD
            self.roi[i] = ref[y:y + h, x:x + w]
            self.roi[i] = cv2.resize(self.roi[i], (57, 88))
            # cv2.imwrite("roi"+str(i)+'o.png',roi)
            self.digits[i] = self.roi[i]
        for idx in range(11):
            self.digits1[idx] = self.digits[idx]
        for idx in range(10):
            self.digits2[idx] = self.digits[idx]
        for idx in range(3):
            self.digits3[idx] = self.digits[11 + idx]

        clone = np.dstack([ref.copy()] * 3)
        for c in refCnt:
            (x, y, w, h) = cv2.boundingRect(c)

            cv2.rectangle(clone, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # roi = ref[y:y + h, x:x + w]
        # cv2.imshow("Simple Method", clone)
        cv2.imshow('roi', self.roi[2])
        # cv2.imshow("test",ref)


    def TextOCR(self):
        Noimg = cv2.imread('no_detect.png')
        while not self.stopEvent.is_set():
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
                                                           cv2.TM_CCOEFF_NORMED)
                                (_, score, _, _) = cv2.minMaxLoc(result)

                                scores.append(score)

                            try:
                                if i == 0:
                                    if str(np.argmax(scores)) == '10':
                                        groupOutput.append('/')
                                    else:
                                        groupOutput.append(str(np.argmax(scores)))

                                elif i == 2:
                                    if str(np.argmax(scores)) == '0':
                                        groupOutput.append('A')
                                    elif str(np.argmax(scores)) == '1':
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

                    img = img2
                    if self.ClickValue == 2:
                        self.Show_panel02_0_1(img)
                        self.Show_panel03_1_0(imgWrap)
                        try:
                            self.Show_panel04_1_1(imgtest2[1])
                        except:
                            pass
                    if self.ClickValue == 10:
                        self.Show_panel01_0_0(self.frameShow)
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
                        self.Show_panel01_0_0(self.frameShow)
                        self.Show_panel03_1_0(Noimg)
                        self.Show_panel05_2_0(Noimg)
                        Label(self.root, text="NONE", width=20, font=("Helvetica", 20)).grid(row=0, column=1)
                        Label(self.root, text="NONE", width=20, font=("Helvetica", 20)).grid(row=1, column=1)
                        Label(self.root, text="NONE", width=20, font=("Helvetica", 20)).grid(row=2, column=1)

    def TextOCR2_no_loop(self):

        if not self.imgOrigin is None:

            start_time = time.time()
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
                y -= 5
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
            scores = []
            total = 0
            ###



            if self.algorithm_flag == 1:
                output = []
                output = self.algorithm1_original_ocr(tmpcnts2, tmpcnts3, locs, output)
                value=self.check_algrithm1(output)
                if value==1:
                    self.pass_value=1
                    Label(self.root, text="PASS", width=5, font=("Helvetica", 16), fg="green").grid(row=3, column=1)
                else:
                    self.fail_value=1
                    Label(self.root, text="FAIL", width=5, font=("Helvetica", 16), fg="red").grid(row=3, column=1)
            elif self.algorithm_flag == 2:
                output = []
                output = self.algorithm2_1(tmpcnts2, locs, output)
                value=self.check_algorithm2_1(output)
                if value==1:
                    self.pass_value=1
                    Label(self.root, text="PASS", width=5, font=("Helvetica", 16), fg="green").grid(row=3, column=1)
                else:
                    self.fail_value=1
                    Label(self.root, text="FAIL", width=5, font=("Helvetica", 16), fg="red").grid(row=3, column=1)
            elif self.algorithm_flag == 3:
                output = []
                self.algorithm2_2(tmpcnts2, tmpcnts3, locs, output)
                value=self.check_algorithm2_2(output)
                if value==1:
                    self.pass_value=1
                    Label(self.root, text="PASS", width=5, font=("Helvetica", 16), fg="green").grid(row=3, column=1)
                else:
                    self.fail_value=1
                    Label(self.root, text="FAIL", width=5, font=("Helvetica", 16), fg="red").grid(row=3, column=1)
            else:
                pass

            img = img2
            if self.ClickValue == 2:
                self.Show_panel02_0_1(img)
                self.Show_panel03_1_0(imgWrap)
                try:
                    self.Show_panel04_1_1(imgtest2[1])
                except:
                    pass
            if self.ClickValue == 10:
                # self.Show_panel01_0_0(self.frameShow)
                self.Show_panel05_2_0(tmpcnts2[1])
                self.Show_panel03_1_0(self.ImgCap)

                try:
                    Label(self.root, text=output[0], width=25, font=("Helvetica", 16)).grid(row=0, column=1)
                    Label(self.root, text=output[1], width=25, font=("Helvetica", 16)).grid(row=1, column=1)
                    Label(self.root, text=output[2], width=25, font=("Helvetica", 16)).grid(row=2, column=1)
                except BaseException as e:
                    print(str(e))
                    pass
            print("---OCR %s seconds ---" % (time.time() - start_time))

    def algorithm1_original_ocr(self, tmpcnts2, tmpcnts3, locs, output):
        imgtest2 = {}
        charac = 0
        kernel = np.ones((1, 1), np.uint8)
        for (i, (gX, gY, gW, gH)) in enumerate(locs):
            groupOutput = []
            img = tmpcnts2[i]

            rectKernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 50))
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
            # imgtest[i] = clone02

            for c in digitCnts:

                (x, y, w, h) = cv2.boundingRect(c)
                ####pad
                x -= 3

                w += 5

                ###pad
                '''x -= 15
                y -= 8
                w += 25
                h += 10'''
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
        imgout=self.digit_cnt_sobel(imgtest2[7])
        self.Show_panel06_3_0(imgout)
        return output

    def algorithm2_1(self, tmpcnts2, locs, output):
        # tmpcnts2 input is tmpcnts3
        for (i, (gX, gY, gW, gH)) in enumerate(locs):
            groupOutput = []
            total2 = 0
            img = tmpcnts2[i]
            ####algorithm2.1
            if i == 0:
                DIGITS = self.area01
            elif i == 1:
                DIGITS = self.area02
            elif i == 2:
                DIGITS = self.area03
            else:
                DIGITS = self.area01

            h, w = DIGITS.shape[:2]
            try:
                img = cv2.resize(img, (w, h))
            except:
                pass
            result = cv2.matchTemplate(img, DIGITS,
                                       cv2.TM_CCORR_NORMED)
            (_, score, _, _) = cv2.minMaxLoc(result)

            gX += 15
            gY += 8
            gW -= 18
            gH -= 10
            output.append(int(score * 100))
        return output

    def algorithm2_2(self, tmpcnts2, tmpcnts3, locs, output):
        imgtest2={}
        charac=0
        kernel = np.ones((1, 1), np.uint8)
        for (i, (gX, gY, gW, gH)) in enumerate(locs):
            groupOutput = []
            total2 = 0
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
            # imgtest[i] = clone02

            for c in digitCnts:

                (x, y, w, h) = cv2.boundingRect(c)
                ####pad
                x -= 3

                w += 5
                ###pad

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
                total = 0
                scores = []
                DIGITS = {}
                if i == 0:
                    DIGITS = self.make01
                elif i == 1:
                    DIGITS = self.make02
                elif i == 2:
                    DIGITS = self.make03
                else:
                    DIGITS = self.digits

                for (digit, digitROI) in DIGITS.items():
                    result = cv2.matchTemplate(roi, digitROI,
                                               cv2.TM_CCOEFF_NORMED)
                    (_, score, _, _) = cv2.minMaxLoc(result)

                    scores.append(int(score * 100))
                    total += int(score * 100)
                groupOutput.append(int(total / int(len(scores))))
                total2 += (total / int(len(scores)))
            gX += 15
            gY += 8
            gW -= 18
            gH -= 10
            output.append(groupOutput)
            #cv2.imshow("test2",imgtest2[0])
        self.Show_panel06_3_0(imgtest2[8])
        return output

    def check_algrithm1(self, output):

        try:
            if (str(self.DateValue) == "".join(str(x) for x in output[0])) and (str(self.NcodeValue) == "".join(str(x) for x in output[1]))and (
                    str(self.CcodeValue) == "".join(str(x) for x in output[2])):
                return 1
            else:
                return 0
        except BaseException as e:
            print(str(e))
            return 0

    def check_algorithm2_1(self, output):
        try:
            if int(output[0]) >= 30 and int(output[1]) >= 30 and int(output[2]) >= 30:
                return 1
            else:
                return 0
        except BaseException as e:
            print(str(e))
            return 0

    def check_algorithm2_2(self, output):
        all_carec = []
        e=0
        e1=1
        try:
            for (idx,i) in enumerate(output) :

                for j in i:
                    all_carec.append(j)
                #print(all_carec)
            for (dx,i) in  enumerate(all_carec):
                if i>= 10 :
                    e=1
                else:
                    e1=0
            return e1
        except BaseException as e:
            print(all_carec)
            print(str(e))
            return 0

    def ocr_thread(self):
        ocrthread = threading.Thread(target=self.TextOCR2_no_loop, args=())
        ocrthread.daemon = True
        ocrthread.start()
        ocrthread.join()

    def no_detect(self):

        if self.ClickValue == 2:
            self.Show_panel02_0_1(self.Noimg)
            self.Show_panel03_1_0(self.Noimg)
            self.Show_panel04_1_1(self.Noimg)
        elif self.ClickValue == 10:
            # self.Show_panel01_0_0(self.frameShow)
            self.Show_panel03_1_0(self.Noimg)
            self.Show_panel05_2_0(self.Noimg)
            Label(self.root, text="NONE", width=20, font=("Helvetica", 20)).grid(row=0, column=1)
            Label(self.root, text="NONE", width=20, font=("Helvetica", 20)).grid(row=1, column=1)
            Label(self.root, text="NONE", width=20, font=("Helvetica", 20)).grid(row=2, column=1)

    def digit_cnt_sobel(self,img):
        thresh=img
        digitCnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                     cv2.CHAIN_APPROX_SIMPLE)
        digitCnts = digitCnts[0] if imutils.is_cv2() else digitCnts[1]
        digitCnts = sorted(digitCnts, key=cv2.contourArea, reverse=True)
        cntt=digitCnts[0]
        leftmost = tuple(cntt[cntt[:, :, 0].argmin()][0])
        rightmost = tuple(cntt[cntt[:, :, 0].argmax()][0])
        topmost = tuple(cntt[cntt[:, :, 1].argmin()][0])
        bottommost = tuple(cntt[cntt[:, :, 1].argmax()][0])
        for cnt in digitCnts:
            leftmostT = tuple(cnt[cnt[:, :, 0].argmin()][0])
            rightmostT = tuple(cnt[cnt[:, :, 0].argmax()][0])
            topmostT = tuple(cnt[cnt[:, :, 1].argmin()][0])
            bottommostT = tuple(cnt[cnt[:, :, 1].argmax()][0])
        cv2.circle(thresh, leftmost, 2, (0, 0, 255), -1)
        cv2.circle(thresh, rightmost, 2, (0, 255, 0), -1)
        cv2.circle(thresh, topmost, 2, (255, 0, 0), -1)
        cv2.circle(thresh, bottommost, 2, (255, 255, 0), -1)
        return thresh
def perspactive_transform(orig, cnts, ratio):
    pts = cnts

    rect = np.zeros((4, 2), dtype="float32")

    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    rect *= ratio

    (tl, tr, br, bl) = rect
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))

    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))

    maxWidth = max(int(widthA), int(widthB))
    maxHeight = max(int(heightA), int(heightB))

    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")

    M = cv2.getPerspectiveTransform(rect, dst)
    warp = cv2.warpPerspective(orig, M, (maxWidth, maxHeight))

    # warp=PIL.Image.fromarray(warp)

    return warp


def pool_perspective(orig, cnts, ratio, threads=2):
    pool = ThreadPool(threads)
    results = pool.map(multi_run_wrapper, [(orig, cnts, ratio)])
    pool.close()
    pool.join()
    results = np.asarray((results[0]), dtype='uint8')
    # cv2.imshow("rrt", results)

    # results=PIL.Image.fromarray(results)
    # print(len(results))
    return results


def tesseract(idx, imgQ):
    img = imgQ.get()
    # l.acquire()

    config = (
        '-c tessedit_char_whitelist=0123456789ABC/ -c tessedit_char_blacklist=abcdefghijklmnopqrstuvwxyzDEFGHIJKLMNOPQRSTOUWXYZ\|-()*^><!$ -l eng --oem 1 --psm 7')
    # img = imgT[i]

    # h, w = img.shape[:2]
    # img = imutils.resize(img, width=int(w / 2), height=int(h / 2))
    # img = gray.get()
    # print("erore")
    t = pytesseract.image_to_string(PIL.Image.fromarray(img[idx]), config=config, lang='eng')
    # Txq.put(t)
    return t
    # print(t)


def multi_run_wrapper(args):
    warp = perspactive_transform(*args)
    return warp


if __name__ == '__main__':
    t = App()
    t.root.mainloop()
