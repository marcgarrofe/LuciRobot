import cv2
from threading import Thread

from picamera.array import PiRGBArray
from picamera import PiCamera

from src.deploy.video.video_module_base import VideoBaseModule
from time import sleep
import numpy as np

import imagezmq

VIDEO_FORMAT = set('avi mp4 mpg mpeg mov mkv wmv'.split())

class VideoInput(VideoBaseModule):

    def __init__(self, video_source, width=640, height=480, use_sockets = False, use_threads = False):
        if hasattr(self, 'th') and self.th.is_alive() or hasattr(self, 'stream') and self.stream.isOpened():
            print("[INFO] Video stream thread already started")
            # self.stop()

        super().__init__()
        self.use_sockets = use_sockets
        self.use_threads = use_threads

        if use_sockets:
            self.image_hub = imagezmq.ImageHub()
        else:
            self.is_picamera = video_source == "picamera"

            self.width = width
            self.height = height

            if not self.is_picamera:
                if  type(video_source) is str:
                    print("[INFO] Opening video file: {}".format(video_source))
                    self.stream = cv2.VideoCapture(video_source)
                else:
                    print("[INFO] Opening camera: {}".format(video_source))
                    self.stream = cv2.VideoCapture(int(video_source))
                    
                self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, width)
                self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

                while self.stream.isOpened() is False:
                    print("[INFO] Waiting for the video file to open...")
                    sleep(0.1)

                if self.stream.isOpened() is False:
                    raise ValueError("Error opening the video file")

                (self.grabbed, self.frame) = self.stream.read()
            
            elif self.is_picamera:
                self.stream =  PiCamera()
                self.stream.resolution = (width, height)
                self.stream.framerate = 32

                # self.raw_capture = PiRGBArray(self.stream, size=(width, height))                       
            
                # allow the camera to warmup
                sleep(0.1)
                
                self.raw_capture = np.empty((width * height * 3), dtype=np.uint8)

                self.stream.capture(self.raw_capture, format="bgr")
                self.frame = self.raw_capture.reshape((height, width, 3))
                
                self.grabbed = len(self.frame) > 0

            self.stopped = False
            self.called = False

    def join(self):
        self.th.join()

    def start(self):
        print("[INFO] Starting video stream thread...")
        self.th = Thread(target=self.get, args=())
        self.th.daemon = True
        self.th.start()

        if self.on_start is not None:
            self.on_start()
        return self

    def get_frame(self):
        # print("[INFO] Reading frame...")
        if self.is_picamera:
            if self.use_sockets:
                rpi_name, image = self.image_hub.recv_image()
            
                if image is not None:
                    self.frame = cv2.imdecode(image, 1)
                    self.grabbed = True
                else:
                    self.grabbed = False
                
                self.image_hub.send_reply(b'OK')
            else:
                self.stream.capture(self.raw_capture, format="bgr", use_video_port=True)
                
                self.frame = self.raw_capture.reshape((self.height, self.width, 3))
                self.grabbed = True
                # clear the numpy array
                self.raw_capture = np.empty((self.width * self.height * 3), dtype=np.uint8)
        else:
            
            
            if self.use_sockets:
                rpi_name, image = self.image_hub.recv_image()
            
                if image is not None:
                    self.frame = cv2.imdecode(image, 1)
                    self.grabbed = True
                else:
                    self.grabbed = False
                
                self.image_hub.send_reply(b'OK')
            else:
                (self.grabbed, self.frame) = self.stream.read()


    def get(self):
        while not self.stopped:
            if not self.grabbed:
                print("Error")
                self.stop()
            else:
                # print("[INFO] Reading frame...")
                if self.is_picamera:
                    if self.use_sockets:
                        rpi_name, image = self.image_hub.recv_image()
                    
                        if image is not None:
                            self.frame = cv2.imdecode(image, 1)
                            self.grabbed = True
                        else:
                            self.grabbed = False
                        
                        self.image_hub.send_reply(b'OK')
                    else:
                        self.stream.capture(self.raw_capture, format="bgr", use_video_port=True)
                        
                        self.frame = self.raw_capture.reshape((self.height, self.width, 3))
                        self.grabbed = True
                        # clear the numpy array
                        self.raw_capture = np.empty((self.width * self.height * 3), dtype=np.uint8)
                else:
                    
                    
                    if self.use_sockets:
                        rpi_name, image = self.image_hub.recv_image()
                    
                        if image is not None:
                            self.frame = cv2.imdecode(image, 1)
                            self.grabbed = True
                        else:
                            self.grabbed = False
                        
                        self.image_hub.send_reply(b'OK')
                    else:
                        (self.grabbed, self.frame) = self.stream.read()

    def stop(self):
        self.stopped = True
    
    def stop(self):
        print("[INFO] Closing video stream...")
        self.stopped = True

        if not self.is_picamera and self.stream.isOpened():
            self.stream.release()
        else:
            self.stream.close()

        if self.on_finish is not None and not self.called:
            self.called = True
            self.on_finish()
        
    def is_opened(self):
        print("[INFO] Checking if video stream is opened...")
        return self.stream.isOpened()

    def __del__(self):
        if not self.is_picamera and self.stream.isOpened():
            self.stream.release()
        else:
            if hasattr(self, 'stream'):
                self.stream.close()