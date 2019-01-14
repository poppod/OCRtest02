import tkinter
import time
import os
import io
from tkinter import *
from tkinter import filedialog, messagebox
from tkinter.font import Font
import pytesseract
import cv2
import threading
import PIL.Image, PIL.ImageTk
import imutils
import multiprocessing
import numpy as np
import queue
import datetime
from  camera_detect import WebcamVideoStream
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
        #self.vs = cv2.VideoCapture(0)
        self.vs= WebcamVideoStream(src=0)
        #####

        self.root = tkinter.Tk()
        self.THsarabun = tkinter.Text(self.root)
        #### time
        self.now = datetime.datetime.now()
        self.root.geometry('800x480')
        self.root.title("ยินดีต้อนรับ")
        self.date_time = str(self.now.strftime("%d-%m-%Y %H:%M"))
        self.date = str(self.now.strftime("%d-%m-%Y"))
        self.start_time = None
        self.end_time = None
        self.start_time_min2cal=None
        self.end_time_min2cal=None
        self.detect_timestamp=0
        self.no_detect_timestamp=0
        ####time
        myfont = Font(family="THSarabunNew", size=14)
        self.THsarabun.configure(font=myfont)
        # self.scale()
        # self.scale2()
        self.root.iconbitmap("./Drawable/icon.ico")
        self.Detect_flag = 0
        self.status_flag = 1
        self.frameShow = None
        self.imgcontoure_selectionSubArea=None
        self.img_tmpcnt4select=None
        self.img_tmpcnt4process=None
        self.frame1 = None
        self.frame = None
        self.thread = None
        self.t1=None

        #####disble when use videoloop_picamera
        #self.ret, self.frameTemp = self.vs.read()
        #####
        self.Noimg = cv2.imread('no_detect.png')
        self.MultiOcr = None
        self.ClickValue = 0
        self.count_sum = 0
        self.pass_value = 0
        self.fail_value = 0
        self.user = None
        self.persentage = 0
        self.detect_finish=IntVar()
        self.value_algor1=None
        self.value_algor2=None
        self.output_algor1=None
        self.log=StringVar()
        self.directory=StringVar()
        self.pass_count = 0
        self.fail_count = 0
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

        self.lock = threading.Lock()
        # self.TextOcrRef()
        self.panel = None
        self.panel2 = None
        self.panel3 = None
        self.panel4 = None
        self.panel5 = None
        self.panel6 = None  # use
        self.buttom = None
        ###### icon
        self.start_icon=None
        self.pause_icon=None
        self.stop_icon=None
        self.power_icon=None
        self.launch_icon=None
        self.setting_icon=None
        self.open_icon=None
        self.edit_icon=None

        self.make01 = None
        self.make02 = None
        self.make03 = None
        self.area01 = None
        self.area02 = None
        self.area03 = None

        self.digits_pad = {}
        self.thresh = queue.Queue()
        self.result = queue.Queue()
        self.stopEvent = threading.Event()
        self.stopEvent2 = threading.Event()
        self.load_all_except_target()
        # self.load_all_value()

        # self.page1_selectOption()
        self.load_icon()
        self.well_com_page()

        # self.page2_selectFile()

        #self.date_realtime()

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
    def load_icon(self):
        icon_list=['./Drawable/play_icon.png','./Drawable/pause_icon.png','./Drawable/stop_icon.png','./Drawable'
                    '/power_icon.ico','./Drawable/launch_icon.ico','./Drawable/setting_icon.ico','./Drawable'
                    '/open_icon.ico','./Drawable/edit_icon.ico']
        icon={}
        for i,x in enumerate(icon_list):
            img= PIL.Image.open(x)
            img = PIL.ImageTk.PhotoImage(img)
            icon[i]=img
        self.start_icon=icon[0]
        self.pause_icon=icon[1]
        self.stop_icon=icon[2]
        self.power_icon=icon[3]
        self.launch_icon=icon[4]
        self.setting_icon=icon[5]
        self.open_icon=icon[6]
        self.edit_icon=icon[7]

    def date_realtime(self):

        self.now = datetime.datetime.now()
        self.date_time = str(self.now.strftime("%Y-%m-%d %H:%M"))
        self.date = str(self.now.strftime("%Y-%m-%d"))
    def information(self):
        msgb=messagebox.showinfo("เกี่ยวกับโปรแกรม","โปรแกรมตรวจสอบคุณภาพฉลากบนผลิตภัณฑ์")
    def well_com_page(self):

        self.root.geometry('800x480')
        self.root.title("ยินดีต้อนรับ")

        info_btn = Button(self.root, text="เกี่ยวกับโปรแกรม", font=("THSarabunNew", 8),command=self.information)  ##command
        info_btn.grid(row=0, column=3)
        help_btn = Button(self.root, text="วิธีใช้", font=("THSarabunNew", 8))  ##command
        help_btn.grid(row=0, column=4)
        well_btn = Label(self.root, text="โปรแกรม ตรวจสอบคุณภาพฉลากบนผลิตภัณฑ์", font=("THSarabunNew", 16))
        well_btn.grid(row=2, column=1, sticky=W + E + N + S, padx=5, pady=5)
        # print(well_btn.winfo_reqwidth())
        Label(self.root, text="ชื่อผู้ใช้งาน หรือผู้ควบคุม", font=("THSarabunNew", 10)).grid(row=3, column=1,
                                                                                             sticky=W + E + N + S,
                                                                                             padx=5, pady=5)
        X = int(((800 - int(well_btn.winfo_reqwidth())) / 15))
        # print(X)
        Label(self.root, width=X + 2).grid(row=0, column=0)
        X = int(X / 3)
        Label(self.root, width=X).grid(row=0, column=2)
        X = int(X - 3)
        Label(self.root, height=X).grid(row=1, column=0)
        vartx = ""
        self.user = Entry(self.root, width=15, textvariable=vartx)  ##data in user no self.user
        self.user.grid(row=4, column=1, sticky=N + S, pady=5)
        login_btn = Button(self.root, text="เข้าสู่โปรแกรม", command=self.well_to_page1)  ##command
        login_btn.grid(row=5, column=1, sticky=N + S, pady=5)

        date = Label(self.root, text=self.date_time, textvariable=self.date_time, font=("THSarabunNew", 8))
        Label(self.root, height=12).grid(row=7, column=0)
        date.grid(row=8, column=3, sticky=E, columnspan=2)
        Button(self.root, image=self.power_icon, command=self.close_program).grid(row=8,column=1)

    def well_to_page1(self):
        user = self.user.get()
        if (user):
            self.user = user
            self.page1_selectOption()
        else:
            messagebox.showerror("Insert Error", "No Value ,Insert value please ")

    def Save_Bbox(self, h, w):
        self.HeightBbox = h
        self.WeightBbox = w

    def Click_ValueBbox(self):
        self.lock.acquire()
        self.ClickValue = 5
        self.lock.release()
        print(5)

    def settingButton(self):
        # self.ClickValue+=1
        self.stopEvent.clear()
        self.stopEvent2.clear()
        self.page2_selectFile()

    def page1_selectOption(self):

        for ele in self.root.winfo_children():
            ele.destroy()


        self.panel = None
        self.panel2 = None
        self.panel3 = None
        self.panel4 = None
        self.root.geometry('800x480')
        self.root.title("Start page")
        user = self.user
        Label(self.root, text="ชื่อผู้ใช้ : " + str(user), font=("THSarabunNew", 12)).grid(row=0, column=1, sticky=W,
                                                                                           padx=5, pady=5, columnspan=2)
        info_btn = Button(self.root, text="เกี่ยวกับโปรแกรม", font=("THSarabunNew", 8))  ##command
        info_btn.grid(row=0, column=6)
        help_btn = Button(self.root, text="วิธีใช้", font=("THSarabunNew", 8))  ##command
        help_btn.grid(row=0, column=7)
        Label(self.root, text="เริ่มต้นการทำงาน", font=("THSarabunNew", 14)).grid(row=2, column=2, sticky=W + E + N + S,
                                                                                  padx=5, pady=5)
        Label(self.root, text="เริ่มต้นการทำงาน โดยใช้ค่าเดิม(ไม่แนะนำ)", font=("THSarabunNew", 10)).grid(row=3,
                                                                                                          column=2,
                                                                                                          sticky=W + E + N + S,
                                                                                                          padx=5,
                                                                                                          pady=5)
        Button(self.root, text='Default',image=self.launch_icon,compound=TOP, command=self.default_process).grid(row=4, column=2, sticky= N + S)
        Label(self.root, text="ตั้งค่าใหม่", font=("THSarabunNew", 14)).grid(row=2, column=4, sticky=W + E + N + S,
                                                                             padx=5, pady=5)
        Label(self.root, text="ตั้งค่าใหม่ ใช้ข้อมูลใหม่(แนะนำ)", font=("THSarabunNew", 10)).grid(row=3, column=4,
                                                                                                  sticky=W + E + N + S,
                                                                                                  padx=5, pady=5)
        Button(self.root, text='Setting',image=self.setting_icon,compound=TOP, command=self.settingButton).grid(row=4, column=4, sticky= N +S)
        date = Label(self.root, text=self.date_time, textvariable=self.date_time, font=("THSarabunNew", 8))
        date.grid(row=8, column=6, sticky=E, columnspan=2)
        Button(self.root, image=self.power_icon, font=("THSarabunNew", 10), command=self.close_program).grid(row=8,
                                                                                                         column=1)
        Label(self.root, width=20, height=8).grid(row=1, column=1)
        Label(self.root, width=10, height=8).grid(row=1, column=3)
        Label(self.root, width=10, height=10).grid(row=5, column=5)

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
            self.panel6 = tkinter.Label(image=img)  ###fix w,h
            self.panel6.image = img
            self.panel6.grid(row=3, column=0)
        else:
            self.panel6.configure(image=img)
            self.panel6.image = img

    def Show_panel_vloop(self, img):
        try:
            img = imutils.resize(img, width=150, height=100)
        except:
            img = img
        img = PIL.Image.fromarray(img)
        img = PIL.ImageTk.PhotoImage(img)
        if self.panel is None:
            self.panel = tkinter.Label(image=img, width=160, height=120)
            self.panel.image = img
            self.panel.grid(row=2, column=1, rowspan=2, columnspan=1, padx=15)
        else:
            self.panel.configure(image=img)
            self.panel.image = img

    def Show_panel_vcap02(self, img):
        try:
            img = imutils.resize(img, width=150, height=100)
        except:
            img = img
        img = PIL.Image.fromarray(img)
        img = PIL.ImageTk.PhotoImage(img)
        if self.panel2 is None:
            self.panel2 = tkinter.Label(image=img, width=160, height=120)
            self.panel2.image = img
            self.panel2.grid(row=5, column=1, rowspan=2, columnspan=1, padx=15)
        else:
            self.panel2.configure(image=img)
            self.panel2.image = img

    def Show_panel_vcap03(self, img):
        try:
            img = imutils.resize(img, width=150, height=100)
        except:
            img = img
        img = PIL.Image.fromarray(img)
        img = PIL.ImageTk.PhotoImage(img)
        if self.panel3 is None:
            self.panel3 = tkinter.Label(image=img, width=160, height=100)
            self.panel3.image = img
            self.panel3.grid(row=8, column=1, rowspan=2, columnspan=1, padx=15)
        else:
            self.panel3.configure(image=img)
            self.panel3.image = img

    def Show_panel_proces01(self, img):
        try:
            img = imutils.resize(img, width=150, height=100)
        except:
            img = img
        img = PIL.Image.fromarray(img)
        img = PIL.ImageTk.PhotoImage(img)
        if self.panel2 is None:
            self.panel2 = tkinter.Label(image=img, width=160, height=100)
            self.panel2.image = img
            self.panel2.grid(row=4, column=4, rowspan=3, columnspan=2, padx=10, pady=15)
        else:
            self.panel2.configure(image=img)
            self.panel2.image = img

    def Show_panel_proces02(self, img):
        try:
            img = imutils.resize(img, width=150, height=100)
        except:
            img = img
        img = PIL.Image.fromarray(img)
        img = PIL.ImageTk.PhotoImage(img)
        if self.panel3 is None:
            self.panel3 = tkinter.Label(image=img, width=160, height=100)
            self.panel3.image = img
            self.panel3.grid(row=4, column=7, rowspan=3, columnspan=3, padx=10, pady=15)
        else:
            self.panel3.configure(image=img)
            self.panel3.image = img

    def importImg(self):
        # img=PIL.Image.open(self.filename)
        def Show_panel_select_page(img):
            try:
                img = imutils.resize(img, width=150, height=100)
            except:
                img = img
            img = PIL.Image.fromarray(img)
            img = PIL.ImageTk.PhotoImage(img)
            if self.panel is None:
                self.panel = tkinter.Label(image=img, width=160, height=120)
                self.panel.image = img
                self.panel.grid(row=6, column=2, columnspan=2, rowspan=2)
            else:
                self.panel.configure(image=img)
                self.panel.image = img

        MegLabel = StringVar()

        img = cv2.imread(self.filename)

        try:
            img2 = img
            # self.Show_panel01_0_0(img)
            Show_panel_select_page(img)
        except:
            self.panel = None
            Nonelabel = Label(self.root, text="None Image").grid(row=6, column=2, columnspan=2, rowspan=2)

        if self.panel is None:

            Nonelabel = Label(self.root, textvariable=MegLabel).grid(row=9, column=2)
            MegLabel.set("None")
        else:
            fileImportButton = Button(self.root, text="Import", command=lambda: self.Save_tempImg(img2)).grid(row=8,
                                                                                                              column=2)
            MegLabel.set("Get Image")
            # Nonelabel.destroy()
            Getlabel = Label(self.root, textvariable=MegLabel).grid(row=9, column=2)

    def Save_tempImg(self, img):
        error = 0
        Msg = messagebox.askyesno("Import and Install ROI", "Do you want to Import and install ROI")
        if Msg == True:
            if img is None:
                NoImportLabel = Label(self.root, text="You do not import Image and install ROI(use default)").grid(
                    row=6, column=3, columnspan=2)
            else:
                cv2.imwrite('./TextRef/temp.png', img=img)  # chang to temp.png
            try:
                self.TextOcrRef()
                error = 0
            except:
                messagebox.showerror(title="File Error", message="File Error Import new file")
                error = 1

        else:
            NoImportLabel = Label(self.root, text="You do not import Image and install ROI(use default)").grid(row=6,
                                                                                                               column=3,
                                                                                                               columnspan=2)
            self.TextOcrRef()
        if error == 0:
            OkNextButton = Button(self.root, text="OK and Next", command=self.page3_setting_vscap).grid(row=8, column=4)

    def reset_bbox(self):
        self.HeightBbox = None
        self.WeightBbox = None

    def page3_setting_vscap(self):
        self.panel = None
        for ele in self.root.winfo_children():
            ele.destroy()
        self.root.title("Setting Video Capture")
        self.ClickValue=0
        user = self.user
        Label(self.root, text="ชื่อผู้ใช้ : " + str(user), font=("THSarabunNew", 12)).grid(row=0, column=0, sticky=W,
                                                                                           padx=5, pady=5, columnspan=2)
        info_btn = Button(self.root, text="เกี่ยวกับโปรแกรม", font=("THSarabunNew", 8))  ##command
        info_btn.grid(row=0, column=11, columnspan=2)
        help_btn = Button(self.root, text="วิธีใช้", font=("THSarabunNew", 8))  ##command
        help_btn.grid(row=0, column=13, columnspan=2)
        Label(self.root, text="ตั้งค่ากล้องวิดีโอ", font=("THSarabunNew", 14)).grid(row=1, column=4,
                                                                                    sticky=W + E + N + S,
                                                                                    padx=5, pady=5, columnspan=4)
        Label(self.root, text="ตั้งค่าคัดกรองสีพื้นหลัง", font=("THSarabunNew", 10)).grid(row=2, column=4,
                                                                                          sticky=W + E + N + S,
                                                                                          padx=5, pady=5, columnspan=3)
        Label(self.root, text="ตั้งค่า contours", font=("THSarabunNew", 10)).grid(row=2, column=8,
                                                                                  sticky=W + E + N + S,
                                                                                  padx=5, pady=5, columnspan=4)
        self.scale()
        self.scale4()
        self.thread = threading.Thread(target=self.videoLoop, args=())
        self.thread.daemon = True
        self.thread.start()
        Label(self.root, width=5, height=2).grid(row=1, column=0)
        date = Label(self.root, text=self.date_time, textvariable=self.date_time, font=("THSarabunNew", 8))
        date.grid(row=11, column=11, sticky=E, columnspan=3)
        BboxSaveButton = Button(self.root, text="Target Area", command=self.Click_ValueBbox).grid(row=9, column=4,
                                                                                                  pady=10)
        ResetBboxSaveButton = Button(self.root, text="Reset", command=self.reset_bbox).grid(row=9, column=5, pady=10)
        OkNextButton = Button(self.root, text="OK and Next", command=self.page3_To_page4).grid(row=9, column=6, pady=10)

    def page3_To_page4(self):
        self.lock.acquire()
        self.ClickValue = 5
        self.lock.release()
        Msg = messagebox.askyesno("Save and Next", "Save target Area and Other setting")
        if Msg == True:
            self.lock.acquire()
            self.ClickValue = 2
            self.lock.release()
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
            #self.ClickValue = 2
            self.page4_settingDigit()

    def page4_settingDigit(self):
        #self.ClickValue = 2
        for ele in self.root.winfo_children():
            ele.destroy()
        self.root.title("Setting Digits")
        self.panel = None
        self.panel2 = None
        self.panel3 = None
        if self.thread.isAlive() == True:
            print("thread Alive")

            user = self.user
            Label(self.root, text="ชื่อผู้ใช้ : " + str(user), font=("THSarabunNew", 12)).grid(row=0, column=0,
                                                                                               sticky=W,
                                                                                               padx=5, pady=5,
                                                                                               columnspan=2)
            Label(self.root, text="ตั้งค่าภาพ", font=("THSarabunNew", 14)).grid(row=1, column=4,
                                                                                sticky=W + E + N + S,
                                                                                padx=5, pady=5, columnspan=4)
            Label(self.root, text="ตั้งค่าสีพื้นหลัง", font=("THSarabunNew", 10)).grid(row=2, column=4,
                                                                                       sticky=W + E + N + S,
                                                                                       padx=5, pady=5,
                                                                                       columnspan=3)
            Label(self.root, text="ตั้งค่า contours", font=("THSarabunNew", 10)).grid(row=2, column=8,
                                                                                      sticky=W + E + N + S,
                                                                                      padx=5, pady=5, columnspan=4)
            self.scale2()
            self.scale3()
            OkNextButton = Button(self.root, text="OK and Next", command=self.page4_To_page5).grid(row=10, column=10)
            info_btn = Button(self.root, text="เกี่ยวกับโปรแกรม", font=("THSarabunNew", 8))  ##command
            info_btn.grid(row=0, column=11, columnspan=2)
            help_btn = Button(self.root, text="วิธีใช้", font=("THSarabunNew", 8))  ##command
            help_btn.grid(row=0, column=13, columnspan=2)
            date = Label(self.root, text=self.date_time, textvariable=self.date_time, font=("THSarabunNew", 8))
            date.grid(row=11, column=11, sticky=E, columnspan=3)
            Label(self.root, width=2, height=0).grid(row=1, column=0)
        else:
            self.stopEvent.clear()
            self.stopEvent2.clear()
            self.thread = threading.Thread(target=self.videoLoop, args=())
            self.thread.daemon = True
            self.thread.start()
            print("dead")

    def page4_To_page5(self):
        self.ClickValue=3
        Msg = messagebox.askyesno("Save and Next", "Save Value and Other setting")
        if Msg == True:
            self.lock.acquire()
            self.ClickValue = 3
            self.lock.release()
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

            #self.ClickValue = 3
            self.page5_Insert_Value()
        else:
            self.ClickValue=2
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
        #self.ClickValue = 3

        self.panel = None
        self.panel2 = None
        self.panel3 = None
        self.panel4 = None


        #self.ClickValue = 3

        for ele in self.root.winfo_children():
            ele.destroy()
        self.root.title("Insert Value")
        user = self.user
        Label(self.root, text="ชื่อผู้ใช้ : " + str(user), font=("THSarabunNew", 12)).grid(row=0, column=0,
                                                                                           sticky=W,
                                                                                           padx=5, pady=5,
                                                                                           columnspan=2)
        Label(self.root, text="ป้อนค่าบนฉลาก", font=("THSarabunNew", 14)).grid(row=2, column=3,
                                                                               sticky=W + E + N + S,
                                                                               padx=5, pady=5, columnspan=4)
        Button(self.root, text="Default load", command=self.load_default_value).grid(row=9, column=4, pady=5)
        Label(self.root, text="Value 1(Date)", font=("THSarabunNew", 10)).grid(row=3, column=3, sticky=W, columnspan=4)
        self.Value1_Entry = Entry(self.root, bd=2, width=30, textvariable=self.DateValue)
        self.Value1_Entry.grid(row=4, column=3, sticky=W, columnspan=4)

        Label(self.root, text="Value 2(Code)", font=("THSarabunNew", 10)).grid(row=5, column=3, sticky=W, columnspan=4)
        self.Value2_Entry = Entry(self.root, bd=2, width=30, textvariable=self.NcodeValue)
        self.Value2_Entry.grid(row=6, column=3, sticky=W, columnspan=4)
        Label(self.root, text="Value 3(Alphabet)", font=("THSarabunNew", 10)).grid(row=7, column=3, sticky=W,
                                                                                   columnspan=4)
        self.Value3_Entry = Entry(self.root, bd=2, width=5, textvariable=self.CcodeValue)
        self.Value3_Entry.grid(row=8, column=3, sticky=W, columnspan=4)
        info_btn = Button(self.root, text="เกี่ยวกับโปรแกรม", font=("THSarabunNew", 8))  ##command
        info_btn.grid(row=0, column=8)
        help_btn = Button(self.root, text="วิธีใช้", font=("THSarabunNew", 8))  ##command
        help_btn.grid(row=0, column=9)
        date = Label(self.root, text=self.date_time, textvariable=self.date_time, font=("THSarabunNew", 8))
        date.grid(row=11, column=8, sticky=E, columnspan=2)
        Button(self.root, text="Save", command=self.save_value_input).grid(row=9, column=5, pady=5)
        Label(self.root, width=20, height=5).grid(row=1, column=2)
        Label(self.root, width=30, height=5).grid(row=1, column=7)

        Label(self.root, width=30, height=8).grid(row=10, column=7)

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
                Ok_Next_button = Button(self.root, text="Ok and Next", command=self.page5_to_process).grid(row=10,
                                                                                                           column=6,
                                                                                                           pady=5)
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
            self.ClickValue=10
            if self.thread.isAlive() == True:
                print("thread Alive")
                # self.thread._Thread_stop()
                self.default_process()
            else:
                print("dead")
                self.stopEvent.clear()
                self.stopEvent2.clear()
                self.default_process()

    def default_process(self):
        for ele in self.root.winfo_children():
            ele.destroy()
            # ele.quit()
        #self.stopEvent.clear()
        self.panel = None
        self.panel2 = None
        self.panel3 = None
        self.panel4 = None
        # self.root2 = tkinter.Tk()
        # self.root2.geometry('800x480')
        self.root.title("Process")
        self.lock.acquire()
        self.ClickValue = 10
        self.lock.release()
        self.TextOcrRef()
        self.load_all_value()

        now=datetime.datetime.now()
        self.start_time_min2cal=(int(now.hour)*60)+int(now.minute)
        self.start_time=str(now.strftime("%H:%M"))
        self.reset_to_new_process()
        self.make_tempplate()
        self.make_tempplate2_no_pad()




        Button(self.root, text="start",image=self.start_icon,compound=RIGHT, command=self.add_algorithm1_flag).grid(row=17, column=7, sticky=W + N + E + S)
        Button(self.root, text="pause",image=self.pause_icon,compound=RIGHT, command=self.add_algorithm2_flag).grid(row=17, column=8, sticky=W + N + E + S)
        Button(self.root, text="stop",image=self.stop_icon,compound=RIGHT, command=self.add_algorithm3_flag).grid(row=17, column=9, sticky=W + N + E + S)
        Button(self.root,image=self.edit_icon, command=self.page5_Insert_Value).grid(row=8, column=8, sticky=W + N + E + S)
        user = self.user
        Label(self.root, text="ชื่อผู้ใช้ : " + str(user), font=("THSarabunNew", 12)).grid(row=0, column=0,
                                                                                           sticky=W,
                                                                                           padx=5, pady=5,
                                                                                           columnspan=2)

        Label(self.root, text="ประมวลผลภาพ", font=("THSarabunNew", 14)).grid(row=2, column=4,
                                                                             sticky=W + E + N + S,
                                                                             padx=5, pady=5, columnspan=5)
        Label(self.root,
              text="ค่าที่ป้อน :  " + str(self.DateValue) + "," + str(self.NcodeValue) + "," + str(self.CcodeValue),
              font=("THSarabunNew", 10)).grid(row=8, column=4, sticky=W, columnspan=4)
        Label(self.root, text="การตรวจจับ :", font=("THSarabunNew", 10)).grid(row=9, column=4, sticky=W, columnspan=2)
        Label(self.root, text="สถานะ :", font=("THSarabunNew", 10)).grid(row=10, column=4, sticky=W)
        Label(self.root, text="ค่าที่อ่านได้ :", font=("THSarabunNew", 10)).grid(row=11, column=4, sticky=W,
                                                                                columnspan=2)
        Label(self.root, text="ค่าความถูกต้อง : 70 %", font=("THSarabunNew", 10)).grid(row=12, column=4, sticky=W,
                                                                                      columnspan=2)
        Label(self.root, text="ความถูกต้องที่อ่านได้ :", font=("THSarabunNew", 10)).grid(row=13, column=4, sticky=W,
                                                                                        columnspan=2)
        Label(self.root, text="ผลลัพธ์ :", font=("THSarabunNew", 10)).grid(row=14, column=4, sticky=W, columnspan=1)
        Label(self.root, text="ทั้งหมด :", font=("THSarabunNew", 10)).grid(row=15, column=4, sticky=W, columnspan=1)
        Label(self.root, text="ผ่าน :", font=("THSarabunNew", 10)).grid(row=16, column=4, sticky=W, columnspan=1)
        Label(self.root, text="ไม่ผ่าน :", font=("THSarabunNew", 10)).grid(row=17, column=4, sticky=W, columnspan=1)
        info_btn = Button(self.root, text="เกี่ยวกับโปรแกรม", font=("THSarabunNew", 10))  ##command
        info_btn.grid(row=0, column=11)
        help_btn = Button(self.root, text="วิธีใช้", font=("THSarabunNew", 10))  ##command
        help_btn.grid(row=0, column=12)
        date = Label(self.root, text=self.date_time, textvariable=self.date_time, font=("THSarabunNew", 10))
        date.grid(row=21, column=11, sticky=E, columnspan=2)
        Label(self.root, width=15, height=0).grid(row=1, column=3)
        Label(self.root, width=10, height=0).grid(row=1, column=10)
        # Label(self.root, width=5, height=5).grid(row=8, column=3)
        if self.thread == None or self.stopEvent.is_set()== True:
            self.stopEvent.clear()
            self.stopEvent2.clear()
            self.thread = threading.Thread(target=self.videoLoop, args=())
            self.thread.daemon = True
            self.thread.start()

            # self.TextOCR()

            '''self.TextocrThread = threading.Thread(target=self.TextOCR, args=())
            self.TextocrThread.daemon = True
            self.TextocrThread.start()'''

        # self.root.destroy()
        # self.root.quit()self.thread.isAlive() == False or

    def reset_to_new_process(self):
        self.status_flag = 2
        self.count_sum = 0
        self.pass_count = 0
        self.fail_count = 0

    def add_algorithm1_flag(self):
        self.status_flag = 1

    def add_algorithm2_flag(self):
        self.status_flag = 2

    def add_algorithm3_flag(self):
        self.status_flag=3
        self.ClickValue=20
        Msg = messagebox.askyesno("Stop", "Stop and close process")
        if Msg==True:
            self.stopEvent.set()
            self.stopEvent2.set()
            self.ClickValue = 20
            self.status_flag = 3
            #print(threading.active_count())
            self.panel = None
            self.panel2 = None
            self.panel3 = None
            self.panel4 = None

            self.save_log_page()
        else:
            self.ClickValue=10
            self.status_flag=2
    def save_log_page(self):
        self.ClickValue = 20

        self.stopEvent.set()
        self.stopEvent2.set()
        for ele in self.root.winfo_children():
            ele.destroy()
            # ele.quit()

        self.panel = None
        self.panel2 = None
        self.panel3 = None
        self.panel4 = None
        #self.ClickValue = 20
        now=datetime.datetime.now()
        self.end_time_min2cal=(int(now.hour)*60)+int(now.minute)
        self.end_time=str(now.strftime("%H:%M"))
        self.root.title("Save Log")
        finish_time=self.end_time_min2cal-self.start_time_min2cal
        user = self.user

        log=[]
        Label(self.root, text="ชื่อผู้ใช้ : " + str(user), font=("THSarabunNew", 12)).grid(row=0, column=0,
                                                                                           sticky=W,
                                                                                           padx=5, pady=5,
                                                                                           columnspan=2)

        Label(self.root, text="วันที่ : " + str(self.date), font=("THSarabunNew", 10)).grid(row=2, column=3, sticky=W,
                                                                                          columnspan=3)

        log.append("DATE:"+ str(self.date))

        Label(self.root, text="ชื่อผู้ใช้ : " + str(user), font=("THSarabunNew", 10)).grid(row=3, column=3, sticky=W,
                                                                                            columnspan=3)
        log.append("USER:" + str(user))

        Label(self.root, text="เริ่ม : " + str(self.start_time), font=("THSarabunNew", 10)).grid(row=4, column=3,
                                                                                            sticky=W,
                                                                                            columnspan=3)
        log.append("START:" + str(self.start_time))

        Label(self.root, text="สิ้นสุด : " + str(self.end_time), font=("THSarabunNew", 10)).grid(row=5, column=3,
                                                                                                 sticky=W,
                                                                                                 columnspan=3)
        log.append("END:" + str(self.end_time))

        Label(self.root, text="ใช้เวลา : " + str(finish_time)+" นาที", font=("THSarabunNew", 10)).grid(row=6, column=3,
                                                                                                 sticky=W,
                                                                                                 columnspan=3)
        log.append("FINISH:" + str(finish_time))

        Label(self.root, text="ทั้งหมด : " + str(self.count_sum), font=("THSarabunNew", 10)).grid(row=7, column=3,
                                                                                                 sticky=W,
                                                                                                 columnspan=3)
        log.append("TOTAL:"+ str(self.count_sum))

        Label(self.root, text="ผ่าน : " + str(self.pass_count), font=("THSarabunNew", 10)).grid(row=8, column=3,
                                                                                                 sticky=W,
                                                                                                 columnspan=3)
        log.append("PASS:"+ str(self.pass_count))

        Label(self.root, text="ไม่ผ่าน : " + str(self.fail_count), font=("THSarabunNew", 10)).grid(row=9, column=3,
                                                                                                 sticky=W,
                                                                                                 columnspan=3)
        log.append("FAIL:"+str(self.fail_count))

        Label(self.root, text="./log/" , font=("THSarabunNew", 8), width=30).grid(row=11, column=3,
                                                                                                   sticky=W,
                                                                                                   columnspan=4)


        Label(self.root,width=30, height=2).grid(row=1, column=2)

        self.log=str(log)

        self.directory='./log/'
        Button(self.root,text="Change", font=("THSarabunNew", 8),command=self.save_dialog).grid(row=11,column=7,sticky=W+N+E+S)
        Button(self.root, text="OK", font=("THSarabunNew", 8), command=self.save_logfile).grid(row=12, column=7,sticky=W+N+E+S)
    def save_dialog(self):
        directory=filedialog.askdirectory(initialdir = './log/')
        self.directory=directory

        if directory:
            Label(self.root, text=str(self.directory), font=("THSarabunNew", 8)).grid(row=11, column=3,
                                                                           sticky=W,
                                                                           columnspan=4)

    def save_logfile(self):
        ms=messagebox.askyesno("Save log","Save log file")
        if ms:
            ms_log=self.log
            self.date_realtime()
            now=datetime.datetime.now()
            nametime = str(now.strftime("(%H-%M)-%d_%m_%Y"))
            path=str(self.directory)+'/'+str(nametime)+'.txt'
            log = open(path,"w")
            log.write(ms_log)
            log.close()
            Label(self.root, text=str(path), font=("THSarabunNew", 8)).grid(row=12, column=3,
                                                                                sticky=W,
                                                                            columnspan=2)

            self.page1_selectOption()
        else:
            return
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
        self.root.geometry('800x480')
        self.root.title("Select File")
        user = self.user
        Label(self.root, text="ชื่อผู้ใช้ : " + str(user), font=("THSarabunNew", 12)).grid(row=0, column=1, sticky=W,
                                                                                           padx=5, pady=5, columnspan=2)
        info_btn = Button(self.root, text="เกี่ยวกับโปรแกรม", font=("THSarabunNew", 8))  ##command
        info_btn.grid(row=0, column=6)
        help_btn = Button(self.root, text="วิธีใช้", font=("THSarabunNew", 8))  ##command
        help_btn.grid(row=0, column=7)
        Label(self.root, text="นำเข้าภาพฟอนต์", font=("THSarabunNew", 14)).grid(row=2, column=2, sticky=W + E + N + S,
                                                                                padx=5, pady=5, columnspan=2)
        Label(self.root, text="นำเข้าใหม่", font=("THSarabunNew", 10)).grid(row=3, column=2, sticky=W + E + N + S,
                                                                            padx=5, pady=5)
        Label(self.root, text="ใช้ค่าเดิม", font=("THSarabunNew", 10)).grid(row=3, column=4, sticky=W + E + N + S,
                                                                            padx=5, pady=5)
        Button(self.root, text="Open File",image=self.open_icon,compound=TOP, command=self.openDialog).grid(row=4, column=2,
                                                                                           sticky=N + S)
        Button(self.root, text="Use default",image=self.launch_icon,compound=TOP, command=self.page2_default_selection).grid(row=4, column=4,
                                                                                                       sticky=N + S)
        date = Label(self.root, text=self.date_time, textvariable=self.date_time, font=("THSarabunNew", 8))
        date.grid(row=10, column=6, sticky=E, columnspan=2)
        Label(self.root, width=38, height=4).grid(row=1, column=1)
        Label(self.root, width=10, height=4).grid(row=1, column=3)
        Label(self.root, width=20, height=0).grid(row=9, column=5)
        Label(self.root, width=20, height=8).grid(row=6, column=5)
        print(self.ClickValue)

    def page2_default_selection(self):
        self.TextOcrRef()
        self.page3_setting_vscap()

    def videoLoop(self):
        def Show_panel_vloop(img):
            try:
                img = imutils.resize(img, width=150, height=100)
            except:
                img = img
            img = PIL.Image.fromarray(img)
            img = PIL.ImageTk.PhotoImage(img)
            if self.panel is None:
                self.panel = tkinter.Label(image=img, width=160, height=120)
                self.panel.image = img
                self.panel.grid(row=2, column=1, rowspan=2, columnspan=1, padx=15)
            else:
                self.panel.configure(image=img)
                self.panel.image = img

        self.vs.start()
        self.frame = self.vs.read()  # temp for fix



        self.start_thread_detect()


        # self.detectThread.join()
        # self.detect()
        try:
            while not self.stopEvent.is_set():

                self.frame = self.vs.read()

                # self.detectThread.run()
                image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                self.frameShow = image
                #cv2.imwrite('./screencapture/img1.png',self.frame)
                #self.detect_noloop()
                if self.ClickValue == 0:
                    Show_panel_vloop(self.frameShow)
                if self.ClickValue == 10:
                    self.Show_panel_proces01(self.frameShow)
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

        scale = Scale(self.root, from_=0, to=255, variable=self.var, label="B", sliderlength=50, length=250)
        scale.set(self.var.get())
        scale1 = Scale(self.root, from_=0, to=255, variable=self.var1, label="G", sliderlength=50, length=250)
        scale1.set(self.var1.get())
        scale2 = Scale(self.root, from_=0, to=255, variable=self.var2, label="R", sliderlength=50, length=250)
        scale2.set(self.var2.get())
        scale.grid(row=3, column=4, rowspan=6, sticky=W + N)
        scale1.grid(row=3, column=5, rowspan=6, sticky=W + N)
        scale2.grid(row=3, column=6, rowspan=6, sticky=W + N)
        '''scale2.pack(fill=BOTH, expand=0, side=RIGHT)
        scale1.pack(fill=BOTH, expand=0, side=RIGHT)
        scale.pack(fill=BOTH, expand=0, side=RIGHT)'''

    def scale2(self):

        scale = Scale(self.root, from_=0, to=255, variable=self.varMax, label="B", sliderlength=50, length=250)
        scale.set(self.varMax.get())
        scale1 = Scale(self.root, from_=0, to=255, variable=self.varMax2, label="G", sliderlength=50, length=250)
        scale1.set(self.varMax2.get())
        scale2 = Scale(self.root, from_=0, to=255, variable=self.varMax3, label="R", sliderlength=50, length=250)
        scale2.set(self.varMax3.get())
        scale3 = Scale(self.root, from_=0, to=255, variable=self.varMax4, label="ความฟุ้ง contours",
                       orient=tkinter.HORIZONTAL, sliderlength=50, length=250)
        scale3.set(self.varMax4.get())
        scale4 = Scale(self.root, from_=0, to=255, variable=self.varMax5, label="ความฟุ้ง digits",
                       orient=tkinter.HORIZONTAL, sliderlength=50, length=250)
        scale4.set(self.varMax5.get())
        scale.grid(row=3, column=4, rowspan=6, sticky=W + N)
        scale1.grid(row=3, column=5, rowspan=6, sticky=W + N)
        scale2.grid(row=3, column=6, rowspan=6, sticky=W + N)
        scale3.grid(row=9, column=3, columnspan=4, sticky=W + N)
        scale4.grid(row=9, column=8, columnspan=6, sticky=W + N)

    def scale3(self):
        # moregrap scale 20 10 18 10

        scale = Scale(self.root, from_=1, to=100, variable=self.rectY, label="rY", sliderlength=50, length=250)
        scale.set(self.rectY.get())
        scale1 = Scale(self.root, from_=1, to=100, variable=self.rectX, label="rX", sliderlength=50, length=250)
        scale1.set(self.rectX.get())
        scale2 = Scale(self.root, from_=1, to=100, variable=self.sqY, label="sqY", sliderlength=50, length=250)
        scale2.set(self.sqY.get())
        scale3 = Scale(self.root, from_=1, to=100, variable=self.sqX, label="sqX", sliderlength=50, length=250)
        scale3.set(self.sqX.get())
        scale.grid(row=3, column=8, rowspan=6, sticky=W + N)
        scale1.grid(row=3, column=9, rowspan=6, sticky=W + N)
        scale2.grid(row=3, column=10, rowspan=6, sticky=W + N)
        scale3.grid(row=3, column=11, rowspan=6, sticky=W + N)

    def scale4(self):  # use vssetting
        # moregrap scale 20 10 18 10

        scale = Scale(self.root, from_=1, to=100, variable=self.rectY2, label="rY", sliderlength=50, length=250)
        scale.set(self.rectY2.get())
        scale1 = Scale(self.root, from_=1, to=100, variable=self.rectX2, label="rX", sliderlength=50, length=250)
        scale1.set(self.rectX2.get())
        scale2 = Scale(self.root, from_=1, to=100, variable=self.sqY2, label="sqY", sliderlength=50, length=250)
        scale2.set(self.sqY2.get())
        scale3 = Scale(self.root, from_=1, to=100, variable=self.sqX2, label="sqX", sliderlength=50, length=250)
        scale3.set(self.sqX2.get())
        scale.grid(row=3, column=8, rowspan=6, sticky=W + N)
        scale1.grid(row=3, column=9, rowspan=6, sticky=W + N)
        scale2.grid(row=3, column=10, rowspan=6, sticky=W + N)
        scale3.grid(row=3, column=11, rowspan=6, sticky=W + N)

    def detect_noloop(self):
        def Show_panel_vcap02(img):
            try:
                img = imutils.resize(img, width=150, height=100)
            except:
                img = img
            img = PIL.Image.fromarray(img)
            img = PIL.ImageTk.PhotoImage(img)
            if self.panel2 is None:
                self.panel2 = tkinter.Label(image=img, width=160, height=120)
                self.panel2.image = img
                self.panel2.grid(row=5, column=1, rowspan=2, columnspan=1, padx=15)
            else:
                self.panel2.configure(image=img)
                self.panel2.image = img

        def Show_panel_vcap03(img):
            try:
                img = imutils.resize(img, width=150, height=100)
            except:
                img = img
            img = PIL.Image.fromarray(img)
            img = PIL.ImageTk.PhotoImage(img)
            if self.panel3 is None:
                self.panel3 = tkinter.Label(image=img, width=160, height=100)
                self.panel3.image = img
                self.panel3.grid(row=8, column=1, rowspan=2, columnspan=1, padx=15)
            else:
                self.panel3.configure(image=img)
                self.panel3.image = img

        self.make_tempplate()
        self.make_tempplate2_no_pad()

        # self.detect_finish=0

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
        self.ImgCap = result
        #cv2.imwrite('./screencapture/detect_perspective.png',self.ImgCap)
        '''if self.ClickValue == 5:
            h1, w1 = result.shape[:2]
            self.Save_Bbox(h1, w1)
            self.ClickValue = 0

        else:
            pass'''

        if self.ClickValue == 0:
            Show_panel_vcap02(self.treshImg)
            Show_panel_vcap03(self.ImgCap)
            # self.Show_panel02_0_1(self.treshImg) ###
            # self.Show_panel03_1_0(self.ImgCap)  #####
        if self.ClickValue == 5:
            h1, w1 = result.shape[:2]
            self.Save_Bbox(h1, w1)
            self.ClickValue = 0
        if self.ClickValue == 2:
            self.TextOCR2_no_loop()

        if self.ClickValue == 10:
            if self.Detect_flag == 1:
                Label(self.root, text="พบ   ", font=("THSarabunNew", 8)).grid(row=9, column=5, sticky=S,
                                                                              columnspan=2)

                self.TextOCR2_no_loop()
            else:
                Label(self.root, text="ไม่พบ", font=("THSarabunNew", 8)).grid(row=9, column=5, sticky=S,
                                                                              columnspan=2)
                self.no_detect()
            if self.status_flag == 1:
                Label(self.root, text="ทำงาน", width=10, font=("THSarabunNew", 8)).grid(row=10, column=5, sticky=W,
                                                                                        )
            elif self.status_flag == 2:
                Label(self.root, text="พัก", width=10, font=("THSarabunNew", 8)).grid(row=10, column=5, sticky=W,
                                                                                      )
            elif self.status_flag == 3:
                Label(self.root, text="หยุดทำงาน", width=10, font=("THSarabunNew", 8)).grid(row=10, column=5,
                                                                                            sticky=W, )

            sum_string = str(self.count_sum)
            Label(self.root, text=sum_string, font=("THSarabunNew", 8)).grid(row=15, column=5)
            pass_string = str(self.pass_count)
            Label(self.root, text=pass_string, font=("THSarabunNew", 8)).grid(row=16, column=5)
            fail_string = str(self.fail_count)
            Label(self.root, text=fail_string, font=("THSarabunNew", 8)).grid(row=17, column=5)
            # self.sum_state.update()
        else:
            pass
        # print(threading.enumerate())
        #print(threading.active_count())
        print("--- %s seconds ---" % (time.time() - start_time))
    def detect(self):


        def Show_panel_vcap02(img):
            try:
                img = imutils.resize(img, width=150, height=100)
            except:
                img = img
            img = PIL.Image.fromarray(img)
            img = PIL.ImageTk.PhotoImage(img)
            if self.panel2 is None:
                self.panel2 = tkinter.Label(image=img, width=160, height=120)
                self.panel2.image = img
                self.panel2.grid(row=5, column=1, rowspan=2, columnspan=1, padx=15)
            else:
                self.panel2.configure(image=img)
                self.panel2.image = img

        def Show_panel_vcap03(img):
            try:
                img = imutils.resize(img, width=150, height=100)
            except:
                img = img
            img = PIL.Image.fromarray(img)
            img = PIL.ImageTk.PhotoImage(img)
            if self.panel3 is None:
                self.panel3 = tkinter.Label(image=img, width=160, height=100)
                self.panel3.image = img
                self.panel3.grid(row=8, column=1, rowspan=2, columnspan=1, padx=15)
            else:
                self.panel3.configure(image=img)
                self.panel3.image = img

        self.make_tempplate()
        self.make_tempplate2_no_pad()

        #self.detect_finish=0
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
            self.ImgCap = result
            '''if self.ClickValue == 5:
                h1, w1 = result.shape[:2]
                self.Save_Bbox(h1, w1)
                self.ClickValue = 0
                
            else:
                pass'''

            if self.ClickValue == 0:
                Show_panel_vcap02(self.treshImg)
                Show_panel_vcap03(self.ImgCap)
                # self.Show_panel02_0_1(self.treshImg) ###
                # self.Show_panel03_1_0(self.ImgCap)  #####
            if self.ClickValue == 5:
                h1, w1 = result.shape[:2]
                self.Save_Bbox(h1, w1)
                self.ClickValue = 0
            if self.ClickValue == 2:
                self.TextOCR2_no_loop()

            if self.ClickValue == 10:
                if self.Detect_flag == 1:
                    Label(self.root, text="พบ   ", font=("THSarabunNew", 8)).grid(row=9, column=5, sticky=W,
                                                                                  )
                    
                    self.TextOCR2_no_loop()
                else:
                    Label(self.root, text="ไม่พบ", font=("THSarabunNew", 8)).grid(row=9, column=5, sticky=W,
                                                                          )
                    self.no_detect()
                if self.status_flag == 1:
                    Label(self.root, text="ทำงาน", width=10, font=("THSarabunNew", 8)).grid(row=10, column=5, sticky=W,
                                                                                            )
                elif self.status_flag == 2:
                    Label(self.root, text="พัก", width=10, font=("THSarabunNew", 8)).grid(row=10, column=5, sticky=W,
                                                                                          )
                elif self.status_flag == 3:
                    Label(self.root, text="หยุดทำงาน", width=10, font=("THSarabunNew", 8)).grid(row=10, column=5,
                                                                                                sticky=W, )

                sum_string = str(self.count_sum)
                Label(self.root, text=sum_string, font=("THSarabunNew", 8)).grid(row=15, column=5)
                pass_string = str(self.pass_count)
                Label(self.root, text=pass_string, font=("THSarabunNew", 8)).grid(row=16, column=5)
                fail_string = str(self.fail_count)
                Label(self.root, text=fail_string, font=("THSarabunNew", 8)).grid(row=17, column=5)
                # self.sum_state.update()
            else:
                pass
            # print(threading.enumerate())
           # print(threading.active_count())
            print("--- %s seconds ---" % (time.time() - start_time))

    def show_attibute_onpage(self):
        def Show_panel_vcap02(img):
            try:
                img = imutils.resize(img, width=150, height=100)
            except:
                img = img
            img = PIL.Image.fromarray(img)
            img = PIL.ImageTk.PhotoImage(img)
            if self.panel2 is None:
                self.panel2 = tkinter.Label(image=img, width=160, height=120)
                self.panel2.image = img
                self.panel2.grid(row=5, column=1, rowspan=2, columnspan=1, padx=15)
            else:
                self.panel2.configure(image=img)
                self.panel2.image = img

        def Show_panel_vcap03(img):
            try:
                img = imutils.resize(img, width=150, height=100)
            except:
                img = img
            img = PIL.Image.fromarray(img)
            img = PIL.ImageTk.PhotoImage(img)
            if self.panel3 is None:
                self.panel3 = tkinter.Label(image=img, width=160, height=100)
                self.panel3.image = img
                self.panel3.grid(row=8, column=1, rowspan=2, columnspan=1, padx=15)
            else:
                self.panel3.configure(image=img)
                self.panel3.image = img

        def Show_panel_vloop(img):
            try:
                img = imutils.resize(img, width=150, height=100)
            except:
                img = img
            img = PIL.Image.fromarray(img)
            img = PIL.ImageTk.PhotoImage(img)
            if self.panel is None:
                self.panel = tkinter.Label(image=img, width=160, height=120)
                self.panel.image = img
                self.panel.grid(row=2, column=1, rowspan=2, columnspan=1, padx=15)
            else:
                self.panel.configure(image=img)
                self.panel.image = img
        while not self.stopEvent2.is_set():
            if self.ClickValue == 0:

                Show_panel_vcap02(self.treshImg)
                Show_panel_vcap03(self.ImgCap)
                Show_panel_vloop(self.frameShow)
            if self.ClickValue==2:

                #from def ocr
                if not self.imgOrigin is None:
                    self.Show_panel_vloop(self.imgcontoure_selectionSubArea)
                    self.Show_panel_vcap02(self.img_tmpcnt4select)
                    self.Show_panel_vcap03(self.img_tmpcnt4process)
            if self.ClickValue == 10:

                self.Show_panel_proces01(self.frameShow)

                if self.Detect_flag == 1:
                    self.Show_panel_proces02(self.ImgCap)
                    Label(self.root, text="พบ   ", font=("THSarabunNew", 8)).grid(row=9, column=5, sticky=W,)
                    ##go to def ocr

                        #self.Show_panel_proces02(self.ImgCap)
                    if self.status_flag == 1:
                        Label(self.root, text="ทำงาน", width=10, font=("THSarabunNew", 8)).grid(row=10, column=5,
                                                                                                sticky=W,
                                                                                                )
                        if (self.value_algor1 or self.value_algor2):
                            self.pass_value = 1
                            Label(self.root, text="PASS", width=5, font=("THSarabunNew", 8), fg="green").grid(row=14,
                                                                                                              column=5)
                        else:
                            self.fail_value = 1
                            Label(self.root, text="FAIL", width=5, font=("THSarabunNew", 8), fg="red").grid(row=14,
                                                                                                            column=5)
                    elif self.status_flag == 2:
                        Label(self.root, text="พัก", width=10, font=("THSarabunNew", 8)).grid(row=10, column=5,
                                                                                              sticky=W,
                                                                                              )
                    elif self.status_flag == 3:
                        Label(self.root, text="หยุดทำงาน", width=10, font=("THSarabunNew", 8)).grid(row=10,
                                                                                                    column=5,
                                                                                                    sticky=W, )


                    try:

                        Label(self.root, text=self.output_algor1, font=("THSarabunNew", 8), width=20).grid(row=11,
                                                                                                           column=5,
                                                                                                           sticky=W,
                                                                                                           columnspan=2)
                        Label(self.root, text=str(self.persentage) + " %", font=("THSarabunNew", 8)).grid(row=13,
                                                                                                          column=5,
                                                                                                          sticky=S,
                                                                                                          columnspan=1)
                    except BaseException as e:
                        print(str(e)+"[p[opoiojk")
                        pass
                else:
                    Label(self.root, text="ไม่พบ", font=("THSarabunNew", 8)).grid(row=9, column=5, sticky=W,
                                                                                  )



                sum_string = str(self.count_sum)
                Label(self.root, text=sum_string, font=("THSarabunNew", 8)).grid(row=15, column=5)
                pass_string = str(self.pass_count)
                Label(self.root, text=pass_string, font=("THSarabunNew", 8)).grid(row=16, column=5)
                fail_string = str(self.fail_count)
                Label(self.root, text=fail_string, font=("THSarabunNew", 8)).grid(row=17, column=5)

    def show_attibute_onpage_thread_start(self):
        self.t1=threading.Thread(target=self.show_attibute_onpage,args=())
        self.t1.daemon=True
        self.t1.start()
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
        #cv2.imwrite('./screencapture/detect_hsv.png',hsv)
        masks = cv2.inRange(hsv, Imin, Imax)
        #cv2.imwrite('./screencapture/detect_masks.png',masks)
        blurred = cv2.blur(masks, (5, 5))

        (_, thresh) = cv2.threshold(blurred, 180, 255, cv2.THRESH_BINARY_INV)
        #cv2.imwrite('./screencapture/detect_colorselection.png',thresh)
        rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (self.rectY2.get(), self.rectX2.get()))
        try:

            sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (self.sqY2.get(), self.sqX2.get()))
        except cv2.error as e:
            # print("error"+str(e))
            sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (34, 11))

        tophat = cv2.morphologyEx(thresh, cv2.MORPH_TOPHAT, rectKernel)
        np.seterr(divide='ignore', invalid='ignore')
        #cv2.imwrite('./screencapture/detect_tophat.png',tophat)
        gradX = cv2.Sobel(tophat, ddepth=cv2.CV_32F, dx=1, dy=0,
                          ksize=7)
        #cv2.imwrite('./screencapture/detect_sobel.png',gradX)
        gradX = np.absolute(gradX)
        #cv2.imwrite('./screencapture/detect_sobelabsolute.png', gradX)
        (minVal, maxVal) = (np.min(gradX), np.max(gradX))

        gradX = (255 * ((gradX - minVal) / (maxVal - minVal)))
        #cv2.imwrite('./screencapture/detect_sobelabsolute_minva.png', gradX)
        gradX = gradX.astype("uint8")
        #cv2.imwrite('./screencapture/detect_sobelabsolute_full.png', gradX)
        gradX = cv2.morphologyEx(gradX, cv2.MORPH_CLOSE, rectKernel)
        #cv2.imwrite('./screencapture/detect_morpho_rect.png', gradX)
        thresh = cv2.threshold(gradX, 0, 255,
                               cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, sqKernel)
        #cv2.imwrite('./screencapture/detect_morpho_sq.png', thresh)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
        #cv2.imwrite('./screencapture/detect_getstruture_kernel.png', kernel)
        closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        #cv2.imwrite('./screencapture/detect_closed.png',closed)
        kernelp = np.ones((15, 15), np.uint8)
        closed = cv2.erode(closed, None, iterations=4)
        closed = cv2.dilate(closed, kernelp, iterations=5)
        #cv2.imwrite('./screencapture/detect_closed_erod_dilate.png',closed)
        _, cnts, hierarchy = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # _, cnts2, hierarchy2 = cv2.findContours(gradient.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # c2 = sorted(cnts2, key=cv2.contourArea, reverse=True)[0]

        clone01 = np.dstack([closed.copy()] * 3)

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

        d_min = 1000
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
            # self.cnt_area_check(cnts[0])
            for c in cnts:
                # approximate the contour
                (x, y, w, h) = cv2.boundingRect(c)
                # self.cnt_area_check(c)
                peri = cv2.arcLength(c, True)
                approx = cv2.approxPolyDP(c, 0.02 * peri, True)
                cv2.rectangle(clone01, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # if our approximated contour has four points, then we
                # can assume that we have found our screen
                if len(approx) == 4:
                    self.cnt_area_check(c)
                    screenCnt = approx
                    break
                else:
                    pass
        else:
            pass
        # screenCnt[1]=screenCnt[1]+20
        self.treshImg = clone01
        #cv2.imwrite('./screencapture/detect_clone01_rectangle.png', clone01)
        if screenCnt is None:
            screenCnt = np.float32([[0, 0], [300, 0], [0, 300], [300, 300]])
            pts = screenCnt.reshape(4, 2)
        else:
            pts = screenCnt.reshape(4, 2)

        if self.ClickValue == 10:
            if self.Detect_flag == 0:
                result = image
            if self.Detect_flag == 1:
                result = self.perspactive_transform(orig, pts, ratio)
            else:
                pass
                # result=pool_perspective(orig,pts,ratio,2)

        else:
            result = self.perspactive_transform(orig, pts, ratio)
            # result = pool_perspective(orig, pts, ratio, 2)
        # result = pool_perspective(orig, pts, ratio, 2)
        return result, image

    def cnt_area_check(self, c):
        x, y, w, h = cv2.boundingRect(c)
        # print(str(w)+" "+str(h))
        if self.ClickValue == 5:
            # h1, w1 = result.shape[:2]
            self.Save_Bbox(h, w)
            self.lock.acquire()
            self.ClickValue = 0
            self.lock.release()
        if not self.HeightBbox is None or not self.WeightBbox is None:
            if h - 20 <= self.HeightBbox <= h + 40 and w - 20 <= self.WeightBbox <= w + 40:

                self.Detect_flag = 1
                self.detect_timestamp = datetime.datetime.now().second
            else:
                if self.Detect_flag == 1:
                    #self.no_detect_timestamp = datetime.datetime.now().second
                    self.change_state()

                self.Detect_flag = 0
                self.no_detect_timestamp=datetime.datetime.now().second

        else:
            pass
        print(self.Detect_flag)

    def change_state(self):
        def_time=self.detect_timestamp-self.no_detect_timestamp
        if self.status_flag == 1 and abs(def_time)>=0.09:

            self.count_sum += 1
            if self.pass_value == 1:
                self.pass_count += 1
            else:
                self.fail_count += 1
            self.pass_value = 0
            self.fail_value = 0
        else:
            pass

    def check_target_area(self):
        image = self.imgOrigin
        h, w = image.shape[:2]

        if not self.HeightBbox is None or not self.WeightBbox is None:
            if h - 20 <= self.HeightBbox <= h + 40:
                if w - 20 <= self.WeightBbox <= w + 40:
                    return 1

                else:
                    return 0
            else:
                # print("fu")
                return 0
        else:
            return 0
            # pass

    def onClose(self):
        # cv2.imwrite("capture.png", self.imgOrigin)
        self.stopEvent.set()
        # self.vs.release()
        self.root.quit()
        # self.root.q
        # exit()
        # self.root.destroy()

    def make_tempplate2_no_pad(self):
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

        # area01 = np.hstack((np.asarray(img) for (ik, img) in make01.items()))

        for idx, digi in enumerate(self.NcodeValue):
            if digi == '/':
                make02[idx] = self.digits[10]
            else:
                for i, img in enumerate(self.digits):
                    if int(digi) == int(i):
                        make02[idx] = self.digits[i]

        # area02 = np.hstack((np.asarray(img) for (ik, img) in make02.items()))

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
        # area03 = np.hstack((np.asarray(img) for (ik, img) in make03.items()))

        # area02 = PIL.Image.fromarray(area02)
        # area03 = PIL.Image.fromarray(area03)
        '''area01.save('./TextRef/Area1.png')
        area02.save('./TextRef/Area2.png')
        area03.save('./TextRef/Area3.png')'''
        # self.area01 = area01
        # self.area02 = area02
        # self.area03 = area03
        self.make01 = make01
        self.make02 = make02
        self.make03 = make03
        # cv2.imwrite('./TextRef/Area1.png', area01)
        # cv2.imwrite('./TextRef/Area2.png', area02)
        # cv2.imwrite('./TextRef/Area3.png', area03)

    def make_tempplate(self):
        make01 = {}
        make02 = {}
        make03 = {}

        for idx, digi in enumerate(self.DateValue):
            if digi == '/':
                make01[idx] = self.digits_pad[10]
            else:
                for (i, img) in enumerate(self.digits_pad):
                    if int(digi) == int(i):
                        make01[idx] = self.digits_pad[i]

        area01 = np.hstack((np.asarray(img) for (ik, img) in make01.items()))

        for idx, digi in enumerate(self.NcodeValue):
            if digi == '/':
                make02[idx] = self.digits_pad[10]
            else:
                for i, img in enumerate(self.digits_pad):
                    if int(digi) == int(i):
                        make02[idx] = self.digits_pad[i]

        area02 = np.hstack((np.asarray(img) for (ik, img) in make02.items()))

        for idx, digi in enumerate(self.CcodeValue):
            if digi == '/':
                make03[idx] = self.digits_pad[10]
            elif digi == 'A':
                make03[idx] = self.digits_pad[11]
            elif digi == 'B':
                make03[idx] = self.digits_pad[12]
            elif digi == 'C':
                make03[idx] = self.digits_pad[13]
            else:
                for i, img in enumerate(self.digits_pad):
                    if int(digi) == int(i):
                        make03[idx] = self.digits_pad[i]
        area03 = np.hstack((np.asarray(img) for (ik, img) in make03.items()))

        # area02 = PIL.Image.fromarray(area02)
        # area03 = PIL.Image.fromarray(area03)
        '''area01.save('./TextRef/Area1.png')
        area02.save('./TextRef/Area2.png')
        area03.save('./TextRef/Area3.png')'''
        self.area01 = area01
        self.area02 = area02
        self.area03 = area03
        # self.make01 = make01
        # self.make02 = make02
        # self.make03 = make03
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
        self.digits_pad = {}
        self.digits = {}
        self.digits1 = {}
        self.digits2 = {}
        self.digits3 = {}
        self.roi = {}
        roi2 = {}
        for (i, c) in enumerate(refCnt):
            (x, y, w, h) = cv2.boundingRect(c)
            ######PAD
            '''x -= 4
            y -= 8
            w += 8
            h += 13'''
            #######PAD
            self.roi[i] = ref[y:y + h, x:x + w]
            self.roi[i] = cv2.resize(self.roi[i], (57, 88))
            self.digits[i] = self.roi[i]
            ######PAD
            x -= 4
            y -= 8
            w += 8
            h += 13
            #######PAD
            # cv2.imwrite("roi"+str(i)+'o.png',roi)
            roi2[i] = ref[y:y + h, x:x + w]
            roi2[i] = cv2.resize(roi2[i], (57, 88))
            self.digits_pad[i] = roi2[i]

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
        # cv2.imshow('roi', self.roi[2])
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
            tmpcnts3 = {}  # ประมวล
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
            self.imgcontoure_selectionSubArea=img
            if self.ClickValue == 2:
                self.Show_panel_vloop(self.imgcontoure_selectionSubArea)

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
                #self.Detect_flag = 0  ##

                tmpcnts2[0] = imgTocrop
                tmpcnts3[0] = imgWrap

            imgtest = {}
            imgtest2 = {}
            charac = 0
            scores = []
            total = 0
            ###

            img = img2
            self.img_tmpcnt4select=img
            self.img_tmpcnt4process=imgWrap
            if self.ClickValue == 2:  ####
                self.Show_panel_vcap02(img)
                self.Show_panel_vcap03(imgWrap)

            if self.ClickValue == 10:
                # self.Show_panel01_0_0(self.frameShow)

                if self.status_flag == 1:
                    output = []
                    output2 = []
                    output = self.algorithm1_original_ocr(tmpcnts2, tmpcnts3, locs, output)
                    output2 = self.algorithm2_2(tmpcnts2, tmpcnts3, locs, output2)
                    value2 = self.check_algorithm2_2(output2)
                    value = self.check_algrithm1(output)
                    self.value_algor1=value
                    self.value_algor2=value2
                    if (self.value_algor1 or self.value_algor2):
                        self.pass_value = 1
                        Label(self.root, text="PASS", width=5, font=("THSarabunNew", 8), fg="green").grid(row=14,
                                                                                                          column=5)
                    else:
                        self.fail_value = 1
                        Label(self.root, text="FAIL", width=5, font=("THSarabunNew", 8), fg="red").grid(row=14,
                                                                                                        column=5)

                else:
                    pass

                self.Show_panel_proces02(self.ImgCap)
                try:
                    out = "".join(str(x) for x in output[0]) + "," + "".join(str(x) for x in output[1]) + "," + "".join(
                        str(x) for x in output[2])
                    self.output_algor1=out
                    Label(self.root, text=self.output_algor1, font=("THSarabunNew", 8), width=20).grid(row=11, column=5, sticky=S,
                                                                                        columnspan=3)
                    Label(self.root, text=str(self.persentage) + " %", font=("THSarabunNew", 8)).grid(row=13, column=5,
                                                                                                      sticky=S,
                                                                                                      columnspan=2)
                except BaseException as e:
                    print(str(e))
                    pass

                '''try:
                    self.Show_panel05_2_0(tmpcnts2[1])
                except:
                    pass

                self.Show_panel03_1_0(self.ImgCap)

                try:
                    Label(self.root, text=output[0], width=25, font=("Helvetica", 16)).grid(row=0, column=1)
                    Label(self.root, text=output[1], width=25, font=("Helvetica", 16)).grid(row=1, column=1)
                    Label(self.root, text=output[2], width=25, font=("Helvetica", 16)).grid(row=2, column=1)
                except BaseException as e:
                    print(str(e))
                    pass'''
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
                roi = self.digit_cnt_sobel(roi)
                roi = cv2.resize(roi, (57, 88))

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
        # imgout=self.digit_cnt_sobel(imgtest2[11])
        # self.Show_panel06_3_0(imgout)
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
        imgtest2 = {}
        charac = 0
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
            DIGITS = {}
            if i == 0:
                DIGITS = self.make01
            elif i == 1:
                DIGITS = self.make02
            elif i == 2:
                DIGITS = self.make03
            else:
                DIGITS = self.digits

            # j=0
            for (j, c) in enumerate(digitCnts):

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
                roi2=roi.copy()
                roi = self.digit_cnt_sobel(roi)
                try:
                    roi = cv2.resize(roi, (57, 88))
                except:
                    roi = cv2.resize(roi2, (57, 88))
                imgtest2[charac] = roi
                charac += 1
                total = 0
                scores = []

                try:
                    digitROI = DIGITS[j]

                    # digitROI=DIGITS[0]
                    # digitROI = cv2.resize(digitROI, (57, 88))
                    # for (digit, digitROI) in DIGITS.items():
                    result = cv2.matchTemplate(roi, digitROI,
                                               cv2.TM_CCOEFF_NORMED)
                    (_, score, _, _) = cv2.minMaxLoc(result)

                    scores.append(int(score * 100))
                    total += int(score * 100)
                    groupOutput.append(int(total / int(len(scores))))
                    total2 += (total / int(len(scores)))
                except:
                    pass
                # j+=1
            gX += 15
            gY += 8
            gW -= 18
            gH -= 10
            output.append(groupOutput)
            # cv2.imshow("test2",imgtest2[0])
        # self.Show_panel06_3_0(imgtest2[8])
        return output

    def check_algrithm1(self, output):

        try:
            if (str(self.DateValue) == "".join(str(x) for x in output[0])) and (
                    str(self.NcodeValue) == "".join(str(x) for x in output[1])) and (
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
        len_carec = []
        e = 0

        try:
            for (idx, i) in enumerate(output):
                len_carec.append(len(i))
                for j in i:
                    all_carec.append(j)
                # print(all_carec)
            min = i[0]
            for (dx, i) in enumerate(all_carec):

                if min >= i:
                    min = i

            if min >= 70:
                e = 1
            else:
                e = 0
            self.persentage = min
            return e
        except BaseException as e1:
            print(all_carec)
            print(str(e1))
            return 0

    def ocr_thread(self):
        ocrthread = threading.Thread(target=self.TextOCR2_no_loop, args=())
        ocrthread.daemon = True
        ocrthread.start()
        ocrthread.join()

    def no_detect(self):

        if self.ClickValue == 2:
            self.Show_panel_vloop(self.Noimg)
            self.Show_panel_vcap02(self.Noimg)
            self.Show_panel_vcap03(self.Noimg)
        elif self.ClickValue == 10:
            # self.Show_panel01_0_0(self.frameShow)
            # self.Show_panel_vcap02(self.Noimg)
            self.Show_panel_proces02(self.Noimg)
            # self.Show_panel05_2_0(self.Noimg)
            '''Label(self.root, text="NONE", width=20, font=("Helvetica", 20)).grid(row=0, column=1)
            Label(self.root, text="NONE", width=20, font=("Helvetica", 20)).grid(row=1, column=1)
            Label(self.root, text="NONE", width=20, font=("Helvetica", 20)).grid(row=2, column=1)'''

    def digit_cnt_sobel(self, img):
        thresh = img
        digitCnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                     cv2.CHAIN_APPROX_SIMPLE)
        digitCnts = digitCnts[0] if imutils.is_cv2() else digitCnts[1]
        digitCnts = sorted(digitCnts, key=cv2.contourArea, reverse=True)
        # print(digitCnts)
        try:
            cntt = digitCnts[0]
            # for cntt in digitCnts:
            leftmost = tuple(cntt[cntt[:, :, 0].argmin()][0])
            rightmost = tuple(cntt[cntt[:, :, 0].argmax()][0])
            topmost = tuple(cntt[cntt[:, :, 1].argmin()][0])
            bottommost = tuple(cntt[cntt[:, :, 1].argmax()][0])
            for cnt in digitCnts:
                leftmostT = tuple(cnt[cnt[:, :, 0].argmin()][0])
                rightmostT = tuple(cnt[cnt[:, :, 0].argmax()][0])
                topmostT = tuple(cnt[cnt[:, :, 1].argmin()][0])
                bottommostT = tuple(cnt[cnt[:, :, 1].argmax()][0])
                # print(leftmost[0])
                if (leftmostT[0] < leftmost[0]):
                    leftmost = list(leftmost)
                    leftmost[0] = leftmostT[0]
                    leftmost = tuple(leftmost)
                if (rightmostT[0] > rightmost[0]):
                    rightmost = list(rightmost)
                    rightmost[0] = rightmostT[0]
                    rightmost = tuple(rightmost)
                if (topmostT[1] < topmost[1]):
                    topmost = list(topmost)
                    topmost[1] = topmostT[1]
                    topmost = tuple(topmost)
                if (bottommostT[1] > bottommost[1]):
                    bottommost = list(bottommost)
                    bottommost[1] = bottommostT[1]
                    bottommost = tuple(bottommost)
            x = leftmost[0]
            y = topmost[1]
            w = rightmost[0] - leftmost[0]
            h = bottommost[1] - topmost[1]
            thresh = thresh[y:y + h, x:x + w]
        except:
            pass

        # cv2.rectangle(thresh, (x, y), (x + w, y + h), (255, 255, 255), 2)
        '''cv2.circle(thresh, leftmost, 2, (0, 0, 255), -1)
        cv2.circle(thresh, rightmost, 2, (0, 255, 0), -1)
        cv2.circle(thresh, topmost, 2, (255, 0, 0), -1)
        cv2.circle(thresh, bottommost, 2, (255, 255, 0), -1)'''

        return thresh

    def perspactive_transform(self, orig, cnts, ratio):
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

    def close_program(self):
        cv2.destroyAllWindows()
        self.stopEvent.set()
        self.root.destroy()


if __name__ == '__main__':
    t = App()
    t.root.mainloop()
