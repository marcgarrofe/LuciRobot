from datetime import datetime
import argparse
import cv2
from threading import Thread

from src.deploy.video.video_module_base import VideoBaseModule


class VideoOutput(VideoBaseModule):
    """
    https://nrsyed.com/2018/07/05/multithreading-with-opencv-python-to-improve-video-processing-performance/
    
    Class that tracks the number of occurrences ("counts") of an
    arbitrary event and returns the frequency in occurrences
    (counts) per second. The caller must increment the count.
    """
    
    def __init__(self, frame=None, name = "Video"):
        super().__init__()
        self.frame = frame
        self.stopped = False
        self.name = name

        
    def start(self):
        Thread(target=self.show, args=()).start()
        if self.on_start is not None:
            self.on_start()
        return self

    def gen_frames():  
        while True:
            if not self.frame:
                break
            else:
                ret, buffer = cv2.imencode('.jpg', self.frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


    def show(self):
        while not self.stopped:
            ret, buffer = cv2.imencode('.jpg', self.frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

    def stop(self):
        self.stopped = True

        if self.on_finish is not None:
            self.on_finish()