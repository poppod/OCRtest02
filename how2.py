import tkinter
import PIL.Image, PIL.ImageTk
import cv2
import imutils
import  io

from tkinter import *
from tkinter import filedialog, messagebox

class Howtouse():
    def __init__(self,master):
        self.root2 =master

        self.root2.geometry('1024x600')
        self.img_pack=None
        self.panel=None
        #self.load_img()
        #self.view()
        self.page=0

        self.root2.wm_protocol("WM_DELETE_WINDOW", self.onClose)
        #self.run()
    def run(self):
        self.load_img()
        self.view()


    def load_img(self):
        self.page=0
        self.img_pack={}
        img_list=['./howtopic/0001.jpg','./howtopic/0002.jpg','./howtopic/0003.jpg','./howtopic/0004.jpg'
                  ,'./howtopic/0005.jpg','./howtopic/0006.jpg','./howtopic/0007.jpg','./howtopic/0008.jpg','./howtopic/0009.jpg'
            , './howtopic/0010.jpg','./howtopic/0011.jpg','./howtopic/0012.jpg','./howtopic/0013.jpg','./howtopic/0014.jpg']
        for i,x in enumerate(img_list):
            img= cv2.imread(x)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            #img=PIL.Image.open(x)
            img = imutils.resize(img, width=1024, height=600)
            img = PIL.Image.fromarray(img)
            img = PIL.ImageTk.PhotoImage(img)



            self.img_pack[i]=img

    def view(self):
        self.root2.geometry('1024x600')
        #self.panel = None
        for ele in self.root2.winfo_children():
            ele.destroy()


        page=self.page
        self.panel = tkinter.Label(self.root2,image=self.img_pack[page], width=1024, height=600)
        self.panel.image = self.img_pack[page]
        #self.panel.place()
        self.panel.place(x=0, y=0)
        Button(self.root2, text="ย้อนกลับ", font=("Noto Sans Thai", 12), command=self.back_btn,
               relief=FLAT, cursor="hand2", background='#F2C94C').place(x=10, y=300)
        Button(self.root2, text="ถัดไป", command=self.next_btn, font=("Noto Sans Thai", 12), relief=FLAT,
               cursor="hand2", background='#26D793').place(x=960, y=300)
        print(self.page)
    def next_btn(self):
        if self.page == 13:
            self.onClose()
        else:
            self.page+=1
            self.view()
    def back_btn(self):
        if self.page<=0:

            self.onClose()
        else:
            self.page-=1
            self.view()
    def onClose(self):

        self.root2.destroy()


if __name__ == '__main__':

   t = Howtouse()
   t.root.mainloop()