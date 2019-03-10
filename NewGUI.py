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
#from pivideostream import PiVideoStream
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
        self.vs= WebcamVideoStream(src=0).start()
        #self.vs=PiVideoStream().start()
        #####

        self.root = tkinter.Tk()
        self.default_font = tkinter.font.Font(family="Ekkamai Standard")
        self.root.option_add("*font",self.default_font)
        #self.THsarabun = tkinter.Text(self.root)
        #### time
        self.now = datetime.datetime.now()
        self.root.geometry('1024x600')
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
        #myfont = Font(family="Ekkamai Standard", size=14)
        #self.THsarabun.configure(font=myfont)
        # self.scale()
        # self.scale2()
        #self.root.iconbitmap('./Drawable/icon.ico')
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

        self.HeightBbox = 0
        self.WeightBbox = 0

        self.rect_cnt_crop=None

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
        self.user_icon=None
        self.manual_icon=None
        self.default_icon=None
        self.setting_small_icon=None

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
        #self.load_all_except_target()
        self.load_all_value()

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
                    '/open_icon.ico','./Drawable/edit_icon.ico','./Drawable/interview.ico','./Drawable/manual.ico'

                   ,'./Drawable/default_icon.ico','./Drawable/setting_small_icon.ico']
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
        self.user_icon=icon[8]
        self.manual_icon=icon[9]
        self.default_icon=icon[10]
        self.setting_small_icon=icon[11]
    def date_realtime(self):

        self.now = datetime.datetime.now()
        self.date_time = str(self.now.strftime("%Y-%m-%d %H:%M"))
        self.date = str(self.now.strftime("%Y-%m-%d"))
    def information(self):
        messagebox.showinfo("เกี่ยวกับโปรแกรม","โปรแกรมตรวจสอบคุณภาพฉลากบนผลิตภัณฑ์")
    def well_com_page(self):

        self.root.geometry('1024x600')
        self.root.title("ยินดีต้อนรับ")
        info_btn = Button(self.root, text="เกี่ยวกับโปรแกรม",font=("Noto Sans Thai",9),command=self.information,relief=FLAT,cursor="hand2")  ##command
        info_btn.place(x=922,y=57)
        Button(self.root, image=self.setting_small_icon, command=self.information, relief=FLAT,
               cursor="hand2").place(x=947,y=10)
        #info_btn.pack()
        help_btn = Button(self.root, text="วิธีการใช้งาน",relief=FLAT,font=("Noto Sans Thai",16),cursor="hand2",background='#C4C4C4')  ##command
        help_btn.place(x=886,y=504)
        well_btn = Label(self.root, text="โปรแกรมตรวจสอบคุณภาพฉลากบนซองบรรจุผลิตภัณฑ์",font=("Noto Sans Thai",30) )
        well_btn.place(x=77,y=89)
        #well_btn.pack()
        # print(well_btn.winfo_reqwidth())
        Label(self.root, text="ชื่อผู้ใช้หรือผู้ควบคุม",font=("Noto Sans Thai",22)).place(x=403,y=148)
        X = int(((800 - int(well_btn.winfo_reqwidth())) / 15))
        # print(X)
        vartx = ""
        self.user = Entry(self.root, width=19, textvariable=vartx,background="#C4C4C4",relief=FLAT)  ##data in user no self.user
        self.user.place(x=407,y=246)
        Label(self.root,image=self.user_icon).place(x=334,y=230)
        login_btn = Button(self.root, text="เข้าสู่ระบบ",relief=FLAT,font=("Noto Sans Thai",16), command=self.well_to_page1,cursor="hand2",background='#26D793')  ##command
        login_btn.place(x=469,y=339)

        '''date = Label(self.root, text=self.date_time, textvariable=self.date_time)
        Label(self.root, height=12).grid(row=7, column=0)
        date.grid(row=8, column=3, sticky=E, columnspan=2)'''
        Label(self.root,image=self.manual_icon).place(x=915,y=425)
        Button(self.root,text="ปิดโปรแกรม", command=self.close_program,relief=FLAT,
               font=("Noto Sans Thai",16),cursor="hand2",background='#F85252').place(x=33,y=504)

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
        Area_configre_H = open('./Configure/AreaH.txt', "w")
        Area_configre_H.write(str(self.HeightBbox))
        Area_configre_H.close()
        Area_configre_W = open('./Configure/AreaW.txt', "w")
        Area_configre_W.write(str(self.WeightBbox))
        Area_configre_W.close()
    def Click_ValueBbox(self):
        result = self.imgOrigin
        h1, w1 = result.shape[:2]
        self.Save_Bbox(h1, w1)


    def settingButton(self):
        # self.ClickValue+=1
        self.stopEvent.clear()
        self.stopEvent2.clear()
        self.page2_selectFile()

    def page1_selectOption(self):
        self.ClickValue = 23
        for ele in self.root.winfo_children():
            ele.destroy()


        self.panel = None
        self.panel2 = None
        self.panel3 = None
        self.panel4 = None
        self.root.geometry('1024x600')
        self.root.title("Start page")
        user = self.user
        Label(self.root, text="ชื่อผู้ใช้ : " + str(user), font=("Noto Sans Thai", 15)).grid(row=0, column=1, sticky=W,
                                                                                           padx=5, pady=5, columnspan=3)
        info_btn = Button(self.root, text="เกี่ยวกับโปรแกรม", font=("Noto Sans Thai", 9), command=self.information,
                          relief=FLAT, cursor="hand2")  ##command
        info_btn.place(x=922, y=57)
        Button(self.root, image=self.setting_small_icon, command=self.information, relief=FLAT,
               cursor="hand2").place(x=947, y=10)

        '''help_btn = Button(self.root, text="วิธีใช้", font=("THSarabunNew", 8))  ##command
        help_btn.grid(row=0, column=7)'''
        Label(self.root, text="เริ่มต้นการทำงาน", font=("Noto Sans Thai", 25)).place(x=159,y=105)
        Label(self.root, text="เริ่มต้นการทำงานโดยใช้ค่าเดิม(ไม่แนะนำ)", font=("Noto Sans Thai", 16)).place(x=107,y=386)
        Button(self.root,image=self.launch_icon, command=self.default_process,relief=FLAT,cursor="hand2").place(x=200,y=166)
        Label(self.root, text='Default',font=("Noto Sans Thai", 16)).place(x=225,y=330)
        Label(self.root, text="ตั้งค่าใหม่", font=("Noto Sans Thai", 25)).place(x=709,y=105)
        Label(self.root, text="ตั้งค่าใหม่ใช้ข้อมูลใหม่(แนะนำ)",font=("Noto Sans Thai", 16)).place(x=641,y=386)
        Button(self.root,image=self.setting_icon, command=self.settingButton,relief=FLAT,cursor="hand2").place(x=709,y=166)
        Label(self.root,text="Setting",font=("Noto Sans Thai", 16)).place(x=733,y=330)
        '''date = Label(self.root, text=self.date_time, textvariable=self.date_time, font=("THSarabunNew", 8))
        date.grid(row=8, column=6, sticky=E, columnspan=2)'''
        Button(self.root,text="ปิดโปรแกรม",font=("Noto Sans Thai", 16), command=self.close_program,relief=FLAT,cursor="hand2",background='#F85252').place(x=455,y=488)
        '''Label(self.root, width=20, height=8).grid(row=1, column=1)
        Label(self.root, width=10, height=8).grid(row=1, column=3)
        Label(self.root, width=10, height=10).grid(row=5, column=5)'''

    def openDialog(self):
        self.filename = filedialog.askopenfilename(initialdir="./", title="Select file",
                                                   filetypes=(("*png files", "*.png"), ("*jpg files", "*.jpg")))
        self.importImg()



    def Show_panel_vloop(self, img):
        try:
            img = imutils.resize(img, width=240, height=135)
        except:
            img = img
        img = PIL.Image.fromarray(img)
        img = PIL.ImageTk.PhotoImage(img)
        if self.panel is None:
            self.panel = tkinter.Label(image=img,width=240, height=135)
            self.panel.image = img
            self.panel.place(x=77,y=67)
        else:
            self.panel.configure(image=img)
            self.panel.image = img

    def Show_panel_vcap02(self, img):
        try:
            img = imutils.resize(img, width=240, height=135)
        except:
            img = img
        img = PIL.Image.fromarray(img)
        img = PIL.ImageTk.PhotoImage(img)
        if self.panel2 is None:
            self.panel2 = tkinter.Label(image=img,width=240, height=135)
            self.panel2.image = img
            self.panel2.place(x=77,y=206)
        else:
            self.panel2.configure(image=img)
            self.panel2.image = img

    def Show_panel_vcap03(self, img):
        try:
            img = imutils.resize(img, width=240, height=135)
        except:
            img = img
        img = PIL.Image.fromarray(img)
        img = PIL.ImageTk.PhotoImage(img)
        if self.panel3 is None:
            self.panel3 = tkinter.Label(image=img,width=240, height=135)
            self.panel3.image = img
            self.panel3.place(x=77,y=345)
        else:
            self.panel3.configure(image=img)
            self.panel3.image = img

    def Show_panel_proces01(self, img):
        try:
            img = imutils.resize(img, width=384, height=216)
        except:
            img = img
        img = PIL.Image.fromarray(img)
        img = PIL.ImageTk.PhotoImage(img)
        if self.panel2 is None:
            self.panel2 = tkinter.Label(image=img,width=384, height=216)
            self.panel2.image = img
            self.panel2.place(x=174,y=116)
        else:
            self.panel2.configure(image=img)
            self.panel2.image = img

    def Show_panel_proces02(self, img):
        try:
            img = imutils.resize(img, width=240, height=135)
        except:
            img = img
        img = PIL.Image.fromarray(img)
        img = PIL.ImageTk.PhotoImage(img)
        if self.panel3 is None:
            self.panel3 = tkinter.Label(image=img,width=240, height=135)
            self.panel3.image = img
            self.panel3.place(x=567,y=116)
        else:
            self.panel3.configure(image=img)
            self.panel3.image = img

    def importImg(self):
        # img=PIL.Image.open(self.filename)
        def Show_panel_select_page(img):
            try:
                img = imutils.resize(img, width=309, height=109)
            except:
                img = img
            img = PIL.Image.fromarray(img)
            img = PIL.ImageTk.PhotoImage(img)
            if self.panel is None:
                self.panel = tkinter.Label(image=img, width=309, height=109)
                self.panel.image = img
                self.panel.place(x=357,y=353)
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
            Label(self.root, text="None Image").place(x=357,y=353)

        if self.panel is None:

            Label(self.root, textvariable=MegLabel).place(x=357,y=353)
            MegLabel.set("None")
        else:
            Button(self.root, text="Import", command=lambda: self.Save_tempImg(img2),relief=FLAT,cursor="hand2",background='#26D793',font=("Noto Sans Thai", 16)).place(x=457,y=474)
            #MegLabel.set("Get Image")
            # Nonelabel.destroy()
            Label(self.root, textvariable=MegLabel).place(x=357,y=353)

    def Save_tempImg(self, img):
        error = 0
        Msg = messagebox.askyesno("Import and Install ROI", "Do you want to Import and install ROI")
        if Msg == True:
            if img is None:
                Label(self.root, text="You do not import Image and install ROI(use default)").place(x=357,y=353)
            else:
                cv2.imwrite('./TextRef/temp.png', img=img)  # chang to temp.png
            try:
                self.TextOcrRef()
                error = 0
            except:
                messagebox.showerror(title="File Error", message="File Error Import new file")
                error = 1

        else:
            Label(self.root, text="You do not import Image and install ROI(use default)").place(x=357,y=353)
            self.TextOcrRef()
        if error == 0:
            Button(self.root, text="OK and Next", command=self.page3_setting_vscap,relief=FLAT,cursor="hand2",background='#26D793',font=("Noto Sans Thai", 16)).place(x=789,y=473)

    def reset_bbox(self):
        self.HeightBbox = 0
        self.WeightBbox = 0
        self.load_all_except_target()
    def page3_setting_vscap(self):
        self.panel = None
        self.panel2 = None
        self.panel3 = None
        self.panel4 = None
        for ele in self.root.winfo_children():
            ele.destroy()
        self.root.geometry('1024x600')
        self.root.title("Setting Video Capture")
        self.ClickValue=0
        user = self.user
        Label(self.root, text="ชื่อผู้ใช้ : " + str(user), font=("Noto Sans Thai", 15)).grid(row=0, column=1, sticky=W,
                                                                                           padx=5, pady=5, columnspan=3)
        info_btn = Button(self.root, text="เกี่ยวกับโปรแกรม",font=("Noto Sans Thai", 9), command=self.information,
                          relief=FLAT, cursor="hand2")  ##command
        info_btn.place(x=922, y=57)
        Button(self.root, image=self.setting_small_icon, command=self.information, relief=FLAT,
               cursor="hand2").place(x=947, y=10)
        '''help_btn = Button(self.root, text="วิธีใช้", font=("THSarabunNew", 8))  ##command
        help_btn.grid(row=0, column=13, columnspan=2)'''
        Label(self.root, text="ตั้งค่ากล้องวิดีโอ", font=("Noto Sans Thai", 30)).place(x=379,y=36)
        Label(self.root, text="ตั้งค่าคัดกรองสีพื้นหลัง",  font=("Noto Sans Thai", 18)).place(x=419,y=130)
        Label(self.root, text="ตั้งค่า contours",font=("Noto Sans Thai", 18)).place(x=765,y=127)
        self.scale()
        self.scale4()
        if self.thread == None or self.stopEvent.is_set()== True:
            self.stopEvent.clear()
            self.stopEvent2.clear()
            self.thread = threading.Thread(target=self.videoLoop, args=())
            self.thread.daemon = True
            self.thread.start()
        Button(self.root, text="ย้อนกลับ", font=("Noto Sans Thai", 16), command=self.back3to2,
               relief=FLAT, cursor="hand2", background='#F2C94C').place(x=40, y=490)
        '''date = Label(self.root, text=self.date_time, textvariable=self.date_time, font=("THSarabunNew", 8))
        date.grid(row=11, column=11, sticky=E, columnspan=3)'''
        Button(self.root, text="Apply", command=self.Click_ValueBbox,font=("Noto Sans Thai", 16),relief=FLAT,cursor="hand2",background='#3BB4F7').place(x=600,y=490)
        Button(self.root, text="Reset", command=self.reset_bbox,font=("Noto Sans Thai", 16),relief=FLAT,cursor="hand2",background='#F85252').place(x=484,y=490)
        Button(self.root, text="OK and Next", command=self.page3_To_page4,font=("Noto Sans Thai", 16),relief=FLAT,cursor="hand2",background='#26D793').place(x=773,y=490)

    def page3_To_page4(self):

        self.ClickValue = 5

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
        self.ClickValue = 2
        for ele in self.root.winfo_children():
            ele.destroy()
        self.root.title("Setting Digits")
        self.root.geometry('1024x600')
        self.panel = None
        self.panel2 = None
        self.panel3 = None
        self.panel4 = None
        if self.thread.isAlive() == True:
            print("thread Alive")

            user = self.user
            Label(self.root, text="ชื่อผู้ใช้ : " + str(user), font=("Noto Sans Thai", 15)).grid(row=0, column=1,
                                                                                                 sticky=W,
                                                                                                 padx=5, pady=5,
                                                                                                 columnspan=3)
            Label(self.root, text="ตั้งค่าภาพ", font=("Noto Sans Thai", 30)).place(x=379,y=36)
            Label(self.root, text="ตั้งค่าสีพื้นหลัง",  font=("Noto Sans Thai", 18)).place(x=419,y=110)
            Label(self.root, text="ตั้งค่า contours", font=("Noto Sans Thai", 18)).place(x=765,y=107)
            Button(self.root, image=self.setting_small_icon, command=self.information, relief=FLAT,
                   cursor="hand2").place(x=947, y=10)
            self.scale2()
            self.scale3()
            Button(self.root, text="OK and Next", command=self.page4_To_page5,font=("Noto Sans Thai", 14),relief=FLAT,cursor="hand2",background='#26D793').place(x=773,y=506)
            info_btn = Button(self.root, text="เกี่ยวกับโปรแกรม", font=("Noto Sans Thai", 9), command=self.information,
                              relief=FLAT, cursor="hand2")  ##command
            info_btn.place(x=922, y=57)
            Button(self.root, text="ย้อนกลับ", font=("Noto Sans Thai", 16), command=self.page3_setting_vscap,
                   relief=FLAT, cursor="hand2", background='#F2C94C').place(x=40, y=490)
            '''help_btn = Button(self.root, text="วิธีใช้", font=("THSarabunNew", 8))  ##command
            help_btn.grid(row=0, column=13, columnspan=2)
            date = Label(self.root, text=self.date_time, textvariable=self.date_time, font=("THSarabunNew", 8))
            date.grid(row=11, column=11, sticky=E, columnspan=3)
            Label(self.root, width=2, height=0).grid(row=1, column=0)'''
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
        Label(self.root, text="ชื่อผู้ใช้ : " + str(user),  font=("Noto Sans Thai", 15)).grid(row=0, column=1,
                                                                                                 sticky=W,
                                                                                                 padx=5, pady=5,
                                                                                                 columnspan=3)
        Label(self.root, text="ป้อนค่าบนฉลาก",  font=("Noto Sans Thai", 30)).place(x=385,y=74)
        Button(self.root, text="Default load", command=self.load_default_value,  font=("Noto Sans Thai", 16),relief=FLAT,cursor="hand2",background='#27AE60').place(x=366,y=423)
        Label(self.root, text="Value 1(Date)",  font=("Noto Sans Thai", 13)).place(x=362,y=159)
        self.Value1_Entry = Entry(self.root, bd=2, width=30, textvariable=self.DateValue,background="#C4C4C4",relief=FLAT)
        self.Value1_Entry.place(x=391,y=191)
        Button(self.root, image=self.setting_small_icon, command=self.information, relief=FLAT,
               cursor="hand2").place(x=947, y=10)
        Label(self.root, text="Value 2(Code)",  font=("Noto Sans Thai", 13)).place(x=362,y=233)
        self.Value2_Entry = Entry(self.root, bd=2, width=30, textvariable=self.NcodeValue,background="#C4C4C4",relief=FLAT)
        self.Value2_Entry.place(x=391,y=263)

        Label(self.root, text="Value 3(Alphabet)", font=("Noto Sans Thai", 13)).place(x=362,y=306)
        self.Value3_Entry = Entry(self.root, bd=2, width=5, textvariable=self.CcodeValue,background="#C4C4C4",relief=FLAT)
        self.Value3_Entry.place(x=391,y=337)
        info_btn = Button(self.root, text="เกี่ยวกับโปรแกรม", font=("Noto Sans Thai", 9), command=self.information,
                          relief=FLAT, cursor="hand2")  ##command
        info_btn.place(x=922, y=57)
        '''help_btn = Button(self.root, text="วิธีใช้", font=("THSarabunNew", 8))  ##command
        help_btn.grid(row=0, column=9)
        date = Label(self.root, text=self.date_time, textvariable=self.date_time, font=("THSarabunNew", 8))
        date.grid(row=11, column=8, sticky=E, columnspan=2)'''
        Button(self.root, text="Save", command=self.save_value_input,  font=("Noto Sans Thai", 16),relief=FLAT,cursor="hand2",background='#3BB4F7').place(x=615, y=423)

        Button(self.root, text="ย้อนกลับ", font=("Noto Sans Thai", 16), command=self.page4_settingDigit,
               relief=FLAT, cursor="hand2", background='#F2C94C').place(x=40, y=490)
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
                Button(self.root, text="Ok and Next", command=self.page5_to_process,font=("Noto Sans Thai", 16),relief=FLAT,cursor="hand2",background='#26D793').place(x=789,y=490)
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
        self.ClickValue = 10

        self.TextOcrRef()
        self.load_all_value()

        now=datetime.datetime.now()
        self.start_time_min2cal=(int(now.hour)*60)+int(now.minute)
        self.start_time=str(now.strftime("%H:%M"))
        self.reset_to_new_process()

        self.make_tempplate2_no_pad()

        Button(self.root, image=self.setting_small_icon, command=self.information, relief=FLAT,
               cursor="hand2").place(x=947, y=10)
        Button(self.root, text="START",width=8, command=self.add_algorithm1_flag,  font=("Noto Sans Thai", 16),relief=FLAT,cursor="hand2",background='#26D793').place(x=180,y=475)
        Button(self.root, text="PAUSE",width=8, command=self.add_algorithm2_flag,font=("Noto Sans Thai", 16),relief=FLAT,cursor="hand2",background='#FFD600').place(x=315,y=475)
        Button(self.root, text="STOP",width=8, command=self.add_algorithm3_flag,font=("Noto Sans Thai", 16),relief=FLAT,cursor="hand2",background='#FF3D00').place(x=451,y=475)
        Button(self.root,text="New value", command=self.edit_insert,font=("Noto Sans Thai", 16),relief=FLAT,cursor="hand2",background='#56CCF2').place(x=629,y=475)
        user = self.user
        Label(self.root, text="ชื่อผู้ใช้ : " + str(user),font=("Noto Sans Thai", 15)).grid(row=0, column=1,
                                                                                                 sticky=W,
                                                                                                 padx=5, pady=5,
                                                                                                 columnspan=3)

        Label(self.root, text="ประมวลผลภาพ",font=("Noto Sans Thai", 30)).place(x=385,y=44)
        Label(self.root,
              text="ค่าที่ป้อน :  " + str(self.DateValue) + "," + str(self.NcodeValue) + "," + str(self.CcodeValue),
              font=("Noto Sans Thai", 13)).place(x=167, y=337)
        Label(self.root, text="การตรวจจับ :",font=("Noto Sans Thai", 16)).place(x=586, y=294)
        Label(self.root, text="สถานะ :", font=("Noto Sans Thai", 16)).place(x=586, y=267)
        Label(self.root, text="ค่าที่อ่านได้ :", font=("Noto Sans Thai", 13)).place(x=167, y=413)
        Label(self.root, text="ค่าความถูกต้อง : 70 %",font=("Noto Sans Thai", 13)).place(x=167, y=361)
        Label(self.root, text="ความถูกต้องที่อ่านได้ :", font=("Noto Sans Thai", 13)).place(x=167, y=385)
        Label(self.root, text="ผลลัพธ์ :",font=("Noto Sans Thai", 16)).place(x=586, y=330)
        Label(self.root, text="ทั้งหมด :",font=("Noto Sans Thai", 16)).place(x=586, y=364)
        Label(self.root, text="ผ่าน :",  fg="#219653",font=("Noto Sans Thai", 16)).place(x=586, y=424)
        Label(self.root, text="ไม่ผ่าน :", fg="#FF0404",font=("Noto Sans Thai", 16)).place(x=586, y=394)
        info_btn = Button(self.root, text="เกี่ยวกับโปรแกรม", font=("Noto Sans Thai", 9), command=self.information,
                          relief=FLAT, cursor="hand2")  ##command
        info_btn.place(x=922, y=57)
        '''help_btn = Button(self.root, text="วิธีใช้", font=("THSarabunNew", 10))  ##command
        help_btn.grid(row=0, column=12)
        date = Label(self.root, text=self.date_time, textvariable=self.date_time, font=("THSarabunNew", 10))
        date.grid(row=21, column=11, sticky=E, columnspan=2)
        Label(self.root, width=15, height=0).grid(row=1, column=3)
        Label(self.root, width=10, height=0).grid(row=1, column=10)'''
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
        Label(self.root,text="บันทึกการทำงาน",font=("Noto Sans Thai", 45)).place(x=313,y=61)
        Label(self.root, text="ชื่อผู้ใช้ : " + str(user),font=("Noto Sans Thai", 15)).grid(row=0, column=1,
                                                                                                 sticky=W,
                                                                                                 padx=5, pady=5,
                                                                                                 columnspan=3)

        Label(self.root, text="วันที่ : " + str(self.date),font=("Noto Sans Thai", 16)).place(x=313,y=155)

        log.append("DATE:"+ str(self.date))

        Label(self.root, text="ชื่อผู้ใช้ : " + str(user),font=("Noto Sans Thai", 16)).place(x=313,y=189)
        log.append("USER:" + str(user))

        Label(self.root, text="เริ่ม : " + str(self.start_time),font=("Noto Sans Thai", 16)).place(x=313,y=223)
        log.append("START:" + str(self.start_time))

        Label(self.root, text="สิ้นสุด : " + str(self.end_time),font=("Noto Sans Thai", 16)).place(x=313,y=257)
        log.append("END:" + str(self.end_time))

        Label(self.root, text="ใช้เวลา : " + str(finish_time)+" นาที",font=("Noto Sans Thai", 16)).place(x=313,y=291)
        log.append("FINISH:" + str(finish_time))

        Label(self.root, text="ทั้งหมด : " + str(self.count_sum),font=("Noto Sans Thai", 16)).place(x=313,y=325)
        log.append("TOTAL:"+ str(self.count_sum))

        Label(self.root, text="ผ่าน : " + str(self.pass_count),font=("Noto Sans Thai", 16)).place(x=313,y=359)
        log.append("PASS:"+ str(self.pass_count))

        Label(self.root, text="ไม่ผ่าน : " + str(self.fail_count),font=("Noto Sans Thai", 16)).place(x=313,y=393)
        log.append("FAIL:"+str(self.fail_count))

        Label(self.root, text="./log/" ,font=("Noto Sans Thai", 14)).place(x=313,y=434)




        self.log=str(log)
        self.stopEvent.set()
        self.stopEvent2.set()
        self.directory='./log/'
        Button(self.root,text="Change",width=10,command=self.save_dialog,font=("Noto Sans Thai", 16),relief=FLAT,cursor="hand2",background='#3BB4F7').place(x=370,y=479)
        Button(self.root, text="OK", width=10,command=self.save_logfile,font=("Noto Sans Thai", 16),relief=FLAT,cursor="hand2",background='#26D793').place(x=611,y=479)
    def save_dialog(self):
        directory=filedialog.askdirectory(initialdir = './log/')
        self.directory=directory

        if directory:
            Label(self.root, text=str(self.directory),font=("Noto Sans Thai", 14)).place(x=313,y=434)
        else:
            self.directory = './log/'
            Label(self.root, text=str(self.directory), font=("Noto Sans Thai", 14)).place(x=313, y=434)

    def edit_insert(self):
        self.status_flag = 2
        self.ClickValue = 3
        ms = messagebox.askyesno("Edit", "Edit Value")
        if ms:
            self.ClickValue = 3
            self.page5_Insert_Value()
        else:
            self.ClickValue = 10

            return
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

    def back3to2(self):
        self.ClickValue = 23
        msg=messagebox.askokcancel("ย้อนกลับ","ต้องการย้อนกลับ")
        if msg==TRUE :
            self.stopEvent.set()
            self.stopEvent2.set()
            self.panel = None
            self.panel2 = None
            self.panel3 = None
            self.panel4 = None
            for ele in self.root.winfo_children():
                ele.destroy()
            self.page2_selectFile()
        else:
            self.ClickValue=0
    def page2_selectFile(self):
        self.ClickValue=23
        self.stopEvent.set()
        self.stopEvent2.set()

        self.panel = None
        for ele in self.root.winfo_children():
            ele.destroy()
        self.ClickValue = 23
        for ele in self.root.winfo_children():
            ele.destroy()
        self.root.geometry('1024x600')
        self.root.title("Select File")
        self.panel = None
        self.panel2 = None
        self.panel3 = None
        self.panel4 = None
        user = self.user
        Label(self.root, text="ชื่อผู้ใช้ : " + str(user), font=("Noto Sans Thai", 15)).grid(row=0, column=1, sticky=W,
                                                                                             padx=5, pady=5,
                                                                                             columnspan=3)
        info_btn = Button(self.root, text="เกี่ยวกับโปรแกรม", font=("Noto Sans Thai", 9), command=self.information,
                          relief=FLAT, cursor="hand2")  ##command
        info_btn.place(x=922, y=57)

        Button(self.root, image=self.setting_small_icon, command=self.information, relief=FLAT,
               cursor="hand2").place(x=947, y=10)
        '''help_btn = Button(self.root, text="วิธีใช้", font=("THSarabunNew", 8))  ##command
        help_btn.grid(row=0, column=7)'''
        Label(self.root, text="นำเข้าภาพฟอนต์", font=("Noto Sans Thai", 30)).place(x=378,y=61)
        Label(self.root, text="นำเข้าใหม่", font=("Noto Sans Thai", 21)).place(x=273,y=134)
        Label(self.root, text="ใช้ค่าเดิม", font=("Noto Sans Thai", 21)).place(x=614,y=134)
        Button(self.root, image=self.open_icon, command=self.openDialog,
                          relief=FLAT, cursor="hand2").place(x=312,y=201)
        Label(self.root,text="Open File",font=("Noto Sans Thai", 16),background='#26D793').place(x=293,y=296)
        Button(self.root,image=self.default_icon, command=self.page2_default_selection,
                          relief=FLAT, cursor="hand2").place(x=632,y=201)
        Label(self.root, text="Use default",font=("Noto Sans Thai", 16),background='#F85252').place(x=599,y=296)

        Button(self.root, text="ย้อนกลับ", font=("Noto Sans Thai", 16), command=self.page1_selectOption,
               relief=FLAT, cursor="hand2",background='#F2C94C').place(x=56,y=474)
        '''date = Label(self.root, text=self.date_time, textvariable=self.date_time, font=("THSarabunNew", 8))
        date.grid(row=10, column=6, sticky=E, columnspan=2)'''
        '''Label(self.root, width=38, height=4).grid(row=1, column=1)
        Label(self.root, width=10, height=4).grid(row=1, column=3)
        Label(self.root, width=20, height=0).grid(row=9, column=5)
        Label(self.root, width=20, height=8).grid(row=6, column=5)'''
        print(self.ClickValue)

    def page2_default_selection(self):
        self.TextOcrRef()
        self.page3_setting_vscap()

    def videoLoop(self):
        def Show_panel_vloop(img):
            try:
                img = imutils.resize(img, width=240, height=135)
            except:
                img = img
            img = PIL.Image.fromarray(img)
            img = PIL.ImageTk.PhotoImage(img)
            if self.panel is None:
                self.panel = tkinter.Label(image=img,width=240, height=135)
                self.panel.image = img
                self.panel.place(x=77,y=67)
            else:
                self.panel.configure(image=img)
                self.panel.image = img

        #self.vs.start() ##forfix
        self.frame = self.vs.read()  # temp for fix



        #self.start_thread_detect()

        self.multi_loop_for_detect()
        # self.detectThread.join()
        # self.detect()


        try:
            while not self.stopEvent.is_set():

                self.frame = self.vs.read()

                # self.detectThread.run()
                image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                self.frameShow = image
                #frame=self.frame
                #cv2.imwrite('./screencapture/img1.png',self.frame)
                #self.detect_noloop()

                if self.ClickValue == 0:
                    Show_panel_vloop(self.frameShow)
                if self.ClickValue == 10:
                    if self.Detect_flag==1 :
                        crop=self.frameShow
                        x=self.rect_cnt_crop[0]+60
                        y=self.rect_cnt_crop[1]+45
                        w=self.rect_cnt_crop[2]+144
                        h=self.rect_cnt_crop[3]+81
                        cv2.rectangle(crop, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        self.Show_panel_proces01(crop)
                    else:
                        self.Show_panel_proces01(self.frameShow)
        except RuntimeError as e:
            print("error runtime")
            self.vs.stop()


    def scale(self):

        scale = Scale(self.root, from_=255, to=0, variable=self.var, sliderlength=50, length=250)
        scale.set(self.var.get())
        scale1 = Scale(self.root, from_=255, to=0, variable=self.var1, sliderlength=50, length=250)
        scale1.set(self.var1.get())
        scale2 = Scale(self.root, from_=255, to=0, variable=self.var2,  sliderlength=50, length=250)
        scale2.set(self.var2.get())
        scale.place(x=405,y=186)
        Label(self.root,text="H").place(x=435,y=444)
        scale1.place(x=480,y=186)
        Label(self.root, text="S").place(x=510, y=444)
        scale2.place(x=555,y=186)
        Label(self.root, text="V").place(x=585, y=444)
        '''scale2.pack(fill=BOTH, expand=0, side=RIGHT)
        scale1.pack(fill=BOTH, expand=0, side=RIGHT)
        scale.pack(fill=BOTH, expand=0, side=RIGHT)'''

    def scale2(self):

        scale = Scale(self.root, from_=255, to=0, variable=self.varMax,  sliderlength=50, length=200)
        scale.set(self.varMax.get())
        scale1 = Scale(self.root, from_=255, to=0, variable=self.varMax2,  sliderlength=50, length=200)
        scale1.set(self.varMax2.get())
        scale2 = Scale(self.root, from_=255, to=0, variable=self.varMax3,  sliderlength=50, length=200)
        scale2.set(self.varMax3.get())
        scale3 = Scale(self.root, from_=0, to=255, variable=self.varMax4, label="ความฟุ้ง contours",
                       orient=tkinter.HORIZONTAL, sliderlength=50, length=250)
        scale3.set(self.varMax4.get())
        scale4 = Scale(self.root, from_=0, to=255, variable=self.varMax5, label="ความฟุ้ง digits",
                       orient=tkinter.HORIZONTAL, sliderlength=50, length=250)
        scale4.set(self.varMax5.get())
        scale.place(x=405, y=166)
        Label(self.root, text="H").place(x=435, y=374)
        scale1.place(x=480, y=166)
        Label(self.root, text="S").place(x=510, y=374)
        scale2.place(x=555, y=166)
        Label(self.root, text="V").place(x=585, y=374)
        scale3.place(x=398, y=408)
        scale4.place(x=672, y=408)

    def scale3(self):
        # moregrap scale 20 10 18 10

        scale = Scale(self.root, from_=100, to=1, variable=self.rectY, sliderlength=50, length=200)
        scale.set(self.rectY.get())
        scale1 = Scale(self.root, from_=100, to=1, variable=self.rectX,  sliderlength=50, length=200)
        scale1.set(self.rectX.get())
        scale2 = Scale(self.root, from_=100, to=1, variable=self.sqY, sliderlength=50, length=200)
        scale2.set(self.sqY.get())
        scale3 = Scale(self.root, from_=100, to=1, variable=self.sqX,  sliderlength=50, length=200)
        scale3.set(self.sqX.get())
        scale.place(x=730, y=166)
        scale1.place(x=786, y=166)
        scale2.place(x=842, y=166)
        scale3.place(x=898, y=166)
        Label(self.root, text="(Size)").place(x=700, y=374)
        Label(self.root, text="Y1").place(x=760, y=374)
        Label(self.root, text="X1").place(x=816, y=374)
        Label(self.root, text="Y2").place(x=872, y=374)
        Label(self.root, text="X2").place(x=928, y=374)

    def scale4(self):  # use vssetting
        # moregrap scale 20 10 18 10

        scale = Scale(self.root, from_=100, to=1, variable=self.rectY2, sliderlength=50, length=250)
        scale.set(self.rectY2.get())
        scale1 = Scale(self.root, from_=100, to=1, variable=self.rectX2,  sliderlength=50, length=250)
        scale1.set(self.rectX2.get())
        scale2 = Scale(self.root, from_=100, to=1, variable=self.sqY2, sliderlength=50, length=250)
        scale2.set(self.sqY2.get())
        scale3 = Scale(self.root, from_=100, to=1, variable=self.sqX2,  sliderlength=50, length=250)
        scale3.set(self.sqX2.get())
        scale.place(x=730,y=186)

        scale1.place(x=786,y=186)
        scale2.place(x=842,y=186)
        scale3.place(x=898,y=186)
        Label(self.root, text="(Size)").place(x=700, y=444)
        Label(self.root, text="Y1").place(x=760, y=444)
        Label(self.root, text="X1").place(x=816, y=444)
        Label(self.root, text="Y2").place(x=872, y=444)
        Label(self.root, text="X2").place(x=928, y=444)

    def detect_noloop(self,image):
        def Show_panel_vcap02(img):
            try:
                img = imutils.resize(img, width=240, height=135)
            except:
                img = img
            img = PIL.Image.fromarray(img)
            img = PIL.ImageTk.PhotoImage(img)
            if self.panel2 is None:
                self.panel2 = tkinter.Label(image=img, width=240, height=135)
                self.panel2.image = img
                self.panel2.place(x=77,y=206)
            else:
                self.panel2.configure(image=img)
                self.panel2.image = img

        def Show_panel_vcap03(img):
            try:
                img = imutils.resize(img, width=240, height=135)
            except:
                img = img
            img = PIL.Image.fromarray(img)
            img = PIL.ImageTk.PhotoImage(img)
            if self.panel3 is None:
                self.panel3 = tkinter.Label(image=img,width=240, height=135)
                self.panel3.image = img
                self.panel3.place(x=77,y=345)
            else:
                self.panel3.configure(image=img)
                self.panel3.image = img


        self.make_tempplate2_no_pad()

        # self.detect_finish=0

        # ret,img= self.vs.read()
        # img=self.frame
        start_time = time.time()

        result, image = self.calculate_detect2(image)
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

        if self.ClickValue == 2:
            self.TextOCR2_no_loop2(result)

        if self.ClickValue == 10:
            if self.Detect_flag == 1:
                Label(self.root, text="พบ   ",  fg="#219653",font=("Noto Sans Thai", 16)).place(x=710, y=294)

                if self.status_flag == 1:
                    self.TextOCR2_no_loop2(result)
                else:
                    self.Show_panel_proces02(self.ImgCap)
            else:
                Label(self.root, text="ไม่พบ", fg="#FF0404", font=("Noto Sans Thai", 16)).place(x=710, y=294)
                Label(self.root, text="           ",width=20, font=("Noto Sans Thai", 13)).place(x=257, y=410)
                Label(self.root, text="           ",width=10, font=("Noto Sans Thai", 13)).place(x=347, y=382)
                self.no_detect()
            if self.status_flag == 1:
                Label(self.root, text="ทำงาน",  fg="#219653", width=10,font=("Noto Sans Thai", 16)).place(x=663, y=267)


            elif self.status_flag == 2:
                Label(self.root, text="พัก", fg="#FF0404", width=10,font=("Noto Sans Thai", 16)).place(x=663, y=267)
            elif self.status_flag == 3:
                Label(self.root, text="หยุดทำงาน", fg="#FF0404", width=10,font=("Noto Sans Thai", 16)).place(x=663, y=267)

            sum_string = str(self.count_sum)
            Label(self.root, text=sum_string, font=("Noto Sans Thai", 16)).place(x=670, y=365)
            pass_string = str(self.pass_count)
            Label(self.root, text=pass_string,  fg="#219653",font=("Noto Sans Thai", 16)).place(x=640, y=424)
            fail_string = str(self.fail_count)
            Label(self.root, text=fail_string, fg="#FF0404",font=("Noto Sans Thai", 16)).place(x=663, y=394)
            # self.sum_state.update().
        else:
            pass
        # print(threading.enumerate())
        #print(threading.active_count())
        print("--- %s seconds ---" % (time.time() - start_time))

    def multi_loop_for_detect(self):
        detectThread = threading.Thread(target=self.loop_for_detect, args=())

        detectThread.daemon = True
        detectThread.start()
    def loop_for_detect(self):

        while not self.stopEvent.is_set():
            frame=self.vs.read()
            #self.detect_noloop(frame)
            t1 = threading.Thread(target=self.detect_noloop, args=(frame,))
            t1.daemon = False
            t1.run()
            print(threading.active_count())

    def calculate_detect2(self,image):

        # self.ret, self.frame = self.vs.read()##change or disble when use picamera

        #image = self.frame
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
        #cv2.imwrite('./screencapture/detect_masks2.png',masks)
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


        screenCnt = None

        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

        # self.cnt_area_check(cnts[0])
        if len(cnts) != 0:
            c = max(cnts, key=cv2.contourArea)
            # approximate the contour
            (x, y, w, h) = cv2.boundingRect(c)
            # self.cnt_area_check(c)

            cv2.rectangle(clone01, (x, y), (x + w, y + h), (0, 255, 0), 2)
            self.rect_cnt_crop=[x,y,w,h]
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)

            self.cnt_area_check(c)
            if (len(approx)==4):
                screenCnt = approx
            else:
                screenCnt=np.float32([[x, y], [x+w, y], [x, y+h], [x+w, y+h]])
        else:pass

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
            self.Detect_flag = 0

            self.ClickValue = 0

        if not self.HeightBbox is 0 or not self.WeightBbox is 0:
            if h - 20 <= self.HeightBbox <= h + 40 and w - 20 <= self.WeightBbox <= w + 40:
                if self.Detect_flag==0 :
                    self.Detect_flag = 1
                    self.detect_timestamp = time.time()
                    print(self.detect_timestamp)
                self.Detect_flag = 1
            else:
                if self.Detect_flag == 1:
                    self.no_detect_timestamp = time.time()
                    self.change_state()

                self.Detect_flag = 0
                self.no_detect_timestamp = 0.000
                self.detect_timestamp = 0.000
                #self.no_detect_timestamp=datetime.datetime.now().second



        print(self.Detect_flag)

    def change_state(self):
        def_time=self.no_detect_timestamp-self.detect_timestamp
        print(def_time)
        if self.status_flag == 1 and abs(def_time) >=0.8:

            self.count_sum += 1
            if self.pass_value == 1:
                self.pass_count += 1
            else:
                self.fail_count += 1
            self.pass_value = 0
            self.fail_value = 0
        else:
            pass
        self.detect_timestamp=0.000
        self.no_detect_timestamp=0.000


    def onClose(self):
        # cv2.imwrite("capture.png", self.imgOrigin)
        self.stopEvent.set()
        self.stopEvent.set()
        self.stopEvent2.set()
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
    def TextOCR2_no_loop2(self,imgOrigin):

        if not imgOrigin is None:

            start_time = time.time()
            rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (self.rectY.get(), self.rectX.get()))
            sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (self.sqY.get(), self.sqX.get()))
            #imgOrigin = self.imgOrigin
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
            self.imgcontoure_selectionSubArea = img
            if self.ClickValue == 2:
                self.Show_panel_vloop(self.imgcontoure_selectionSubArea)

            output = []


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
                # self.Detect_flag = 0  ##
                #return
                tmpcnts2[0] = imgTocrop
                tmpcnts3[0] = imgWrap


            ###

            img = img2
            self.img_tmpcnt4select = img
            self.img_tmpcnt4process = imgWrap
            if self.ClickValue == 2:  ####
                self.Show_panel_vcap02(img)
                self.Show_panel_vcap03(imgWrap)

            if self.ClickValue == 10:
                # self.Show_panel01_0_0(self.frameShow)
                self.Show_panel_proces02(self.ImgCap)
                if len(tmpcnts) != 3:
                    return
                if len(tmpcnts3) > 19:
                    return
                if self.status_flag == 1:
                    if len(tmpcnts) > 3:
                        self.fail_value = 1
                        pass
                    elif len(tmpcnts3) > 19:
                        self.fail_value = 1
                        pass
                    else:
                        output = []
                        output2 = []
                        output = self.algorithm1_original_ocr(tmpcnts2, tmpcnts3, locs, output)
                        output2 = self.algorithm2_2(tmpcnts2, tmpcnts3, locs, output2)
                        value2 = self.check_algorithm2_2(output2)
                        value = self.check_algrithm1(output)
                        self.value_algor1 = value
                        self.value_algor2 = value2
                        if (self.value_algor1 or self.value_algor2):
                            self.pass_value = 1
                            Label(self.root, text="PASS", width=5,  fg="#219653",font=("Noto Sans Thai", 16)).place(x=670, y=330)
                        else:
                            self.fail_value = 1
                            Label(self.root, text="FAIL", width=5, fg="#FF0404",font=("Noto Sans Thai", 16)).place(x=670, y=330)

                else:
                    pass


                try:
                    out = "".join(str(x) for x in output[0]) + "," + "".join(str(x) for x in output[1]) + "," + "".join(
                        str(x) for x in output[2])
                    self.output_algor1 = out
                    Label(self.root, text=self.output_algor1,width=20, font=("Noto Sans Thai", 13)).place(x=257, y=410)
                    Label(self.root, text=str(self.persentage) + " %",width=5,  font=("Noto Sans Thai", 13)).place(x=347, y=382)
                except BaseException as e:
                    print(str(e) + "poppy")
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

        return
    def algorithm1_original_ocr(self, tmpcnts2, tmpcnts3, locs, output):
        imgtest2 = {}
        charac = 0
        kernel = np.ones((1, 1), np.uint8)
        for (i, (gX, gY, gW, gH)) in enumerate(locs):
            groupOutput = []
            img = tmpcnts2[i]

            rectKernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 60))
            sqKernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 60))
            tophat2 = cv2.morphologyEx(img, cv2.MORPH_TOPHAT, rectKernel2)

            np.seterr(divide='ignore', invalid='ignore')
            gradX = cv2.Sobel(tophat2, ddepth=cv2.CV_32F, dx=0, dy=1, ksize=3)
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
                #x -= 3

                #w += 5

                ###pad
                '''x -= 15
                y -= 8
                w += 25
                h += 10'''
                #cv2.rectangle(clone02, (x, y), (x + w, y + h), (0, 255, 0), 2)
                roi = tmpcnts3[i][y:y + h, x:x + w]
                roi = cv2.morphologyEx(roi, cv2.MORPH_OPEN, kernel)
                roi = cv2.morphologyEx(roi, cv2.MORPH_CLOSE, kernel)
                roi = cv2.dilate(roi, kernel, iterations=1)
                try:
                    roi = cv2.resize(roi, (57, 88))
                except:
                    pass
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
                                               cv2.TM_SQDIFF_NORMED)
                    (_, score, _, _) = cv2.minMaxLoc(result)

                    scores.append(score)
                #cv2.imwrite("./screencapture/"+str(c[0])+".png",roi)
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



    def algorithm2_2(self, tmpcnts2, tmpcnts3, locs, output):
        imgtest2 = {}
        charac = 0
        kernel = np.ones((1, 1), np.uint8)
        for (i, (gX, gY, gW, gH)) in enumerate(locs):
            groupOutput = []
            total2 = 0
            img = tmpcnts2[i]
            rectKernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 60))
            sqKernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 60))
            tophat2 = cv2.morphologyEx(img, cv2.MORPH_TOPHAT, rectKernel2)

            np.seterr(divide='ignore', invalid='ignore')
            gradX = cv2.Sobel(tophat2, ddepth=cv2.CV_32F, dx=0, dy=1, ksize=3)
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
                #x -= 3

                #w += 5
                ###pad

                #cv2.rectangle(clone02, (x, y), (x + w, y + h), (0, 255, 0), 2)
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
                                               cv2.TM_CCORR_NORMED)
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


    def check_algorithm2_2(self, output):
        all_carec = []
        len_carec = []


        try:
            for (idx, i) in enumerate(output):
                len_carec.append(len(i))
                for j in i:
                    all_carec.append(j)
                # print(all_carec)

            v_max=max(all_carec)
            v_min=min(all_carec)

            everage=sum(all_carec)/len(all_carec)
            if v_min >= 70:
                e = 1
            else:
                e = 0
            self.persentage = int(v_min)
            return e
        except BaseException as e1:
            print(all_carec)
            print(str(e1))
            return 0


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
        self.vs.stop()
        self.stopEvent.set()
        self.root.destroy()


if __name__ == '__main__':

    t = App()
    t.root.mainloop()
