from tkinter import *
import time
import threading

class ScaleValue:
    def __init__(self):
        self.value1 = None
        self.value2 = None

def tkinter_loop(scale):
    root=Tk()
    s1 = Scale(root, from_=0, to=42, tickinterval=8, command=lambda v: setattr(scale, 'value1', v))
    s1.set(19)
    s1.pack()
    s2 = Scale(root, from_=0, to=200, length=600, tickinterval=10, orient=HORIZONTAL, command=lambda v: setattr(scale, 'value2', v))
    s2.set(23)
    s2.pack()
    root.mainloop()

scale = ScaleValue()
threading.Thread(target=tkinter_loop, args=(scale,)).start()

# ROP
while 1:
    #time.sleep(0.1)
    print (scale.value1, scale.value2)