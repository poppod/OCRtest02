import tkinter
from tkinter import *
import cv2
import threading
import PIL.Image, PIL.ImageTk
#import imu

class App():
    def __init__(self,):

        self.vs=cv2.VideoCapture(1)
        self.root=tkinter.Tk()
        self.scale()
        self.frame = None
        self.thread = None
        self.stopEvent = None
        self.panel=None
        self.panel2=None
        self.panel3=None
        self.stopEvent= threading.Event()
        self.thread=threading.Thread(target=self.videoLoop, args=())
        self.thread.start()
        #self.scale()
        self.root.wm_protocol("WM_DELETE_WINDOW",self.onClose)
    def videoLoop(self):

        try:
            while not self.stopEvent.is_set():
                self.ret,self.frame=self.vs.read()
                image=cv2.cvtColor(self.frame,cv2.COLOR_BGR2RGB)
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
        scale = Scale(self.root, from_=0, to=255, variable=self.var)
        scale.set(0)
        scale1 = Scale(self.root, from_=0, to=255, variable=self.var1)
        scale1.set(0)
        scale2 = Scale(self.root, from_=0, to=255, variable=self.var2)
        scale2.set(180)
        scale2.pack(fill=BOTH, expand=0, side=RIGHT)
        scale1.pack(fill=BOTH, expand=0, side=RIGHT)
        scale.pack(fill=BOTH, expand=0, side=RIGHT)



    def onClose(self):
        self.stopEvent.set()
        #self.vs.stop()
        self.root.quit()
        exit()
        #self.root.destroy()

t=App()
t.root.mainloop()





