import cv2
from threading import Thread

from src.deploy.video.video_module_base import VideoBaseModule
from time import sleep

VIDEO_FORMAT = set('avi mp4 mpg mpeg mov mkv wmv'.split())

class VideoInput(VideoBaseModule):

    def __init__(self, video_source, width=640, height=480,):
        super().__init__()
        
        if type(video_source) is str:
            print("[INFO] Opening video file: {}".format(video_source))
            self.stream = cv2.VideoCapture(video_source)
        else:
            print("[INFO] Opening camera: {}".format(video_source))
            self.stream = cv2.VideoCapture(int(video_source))

        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        # while self.stream.isOpened() is False:
        #     sleep(0.1)

        if self.stream.isOpened() is False:
            raise ValueError("Error opening the video file")

        (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False

    def start(self):
        print("[INFO] Starting video stream thread...")
        Thread(target=self.get, args=()).start()
        if self.on_start is not None:
            self.on_start()
        return self

    def get(self):
        while not self.stopped:
            if not self.grabbed:
                self.stop()
            else:
                (self.grabbed, self.frame) = self.stream.read()

    def stop(self):
        self.stopped = True
    
    def stop(self):
        print("[INFO] Closing video stream...")
        self.stopped = True

        if self.stream.isOpened():
            self.stream.release()

        if self.on_finish is not None:
            self.on_finish()
        
    def is_opened(self):
        print("[INFO] Checking if video stream is opened...")
        return self.stream.isOpened()

    def __del__(self):
        self.stream.release()