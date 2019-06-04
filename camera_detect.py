from threading import Thread
import cv2


class WebcamVideoStream:
    def __init__(self, src=0):
        # initialize the video camera stream and read the first frame
        # from the stream
        self.stream = cv2.VideoCapture(src+cv2.CAP_DSHOW)
        self.stream.set(cv2.CAP_PROP_FOURCC,1196444237.0)
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.stream.set(cv2.CAP_PROP_FPS,30.0)
        self.stream.set(cv2.CAP_PROP_BRIGHTNESS,200)
        (self.grabbed, self.frame) = self.stream.read()

        # initialize the variable used to indicate if the thread should
        # be stopped
        self.stopped = False

    def start(self) -> object:
        # start the thread to read frames from the video stream
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        # keep looping infinitely until the thread is stopped
        while True:
            # if the thread indicator variable is set, stop the thread
            if self.stopped:
                return

            # otherwise, read the next frame from the stream
            (self.grabbed, self.frame) = self.stream.read()
            fps = self.stream.get(cv2.CAP_PROP_FPS)
            bri=self.stream.get(cv2.CAP_PROP_BRIGHTNESS)
            w=self.stream.get(cv2.CAP_PROP_FRAME_WIDTH)
            h=self.stream.get(cv2.CAP_PROP_FRAME_HEIGHT)
            mode=self.stream.get(cv2.CAP_PROP_FOURCC)
            '''print('FPS : {0}'.format(fps))
            print('BRIGHTNESS : {0}'.format(bri))
            print('W :{0} h :{1}'.format(w,h))
            print('mode : {0}'.format(mode))'''
    def read(self):
        # return the frame most recently read
        return self.frame

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True