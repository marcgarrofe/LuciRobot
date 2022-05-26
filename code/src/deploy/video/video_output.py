from datetime import datetime
import argparse
import cv2
from threading import Thread

from src.deploy.video.video_module_base import VideoBaseModule
from src.deploy.video.video_fps import VideoFPS

from src.computer_vision.object_detector.hog_detector import people_detectorHOG
from src.computer_vision.object_detector.ssd_detector import people_detectorSSD
from subprocess import PIPE, Popen

# from gpiozero import CPUTemperature 


class VideoOutput(VideoBaseModule):
    """
    https://nrsyed.com/2018/07/05/multithreading-with-opencv-python-to-improve-video-processing-performance/
    
    Class that tracks the number of occurrences ("counts") of an
    arbitrary event and returns the frequency in occurrences
    (counts) per second. The caller must increment the count.
    """
    
    def __init__(self, frame=None, name = "Video", type_detector="SSD"):
        super().__init__()
        self.frame = frame
        self.stopped = False
        self.name = name
        self.vid_fps = VideoFPS().start() # inicialitzem el sistema que calcula els frames per segon


        self.type_detector = type_detector
        if type_detector == "SSD":
            self.people_detector = people_detectorSSD()     # Xarxa neuronal
        elif type_detector == "HOG":
            self.people_detector = people_detectorHOG()   # Histograma de Gradients
        elif type_detector != "None":
            raise ValueError("[ERROR] : Tipus de detector (type_detector) pot ser (SSD, HOG, None)")
        
        
    def start(self):
        # Thread(target=self.show, args=()).start()
        if self.on_start is not None:
            self.on_start()
        return self

    def get_cpu_temperature(self):
        """get cpu temperature using vcgencmd"""
        process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE)
        output, _error = process.communicate()
        return float(output[output.index('=') + 1:output.rindex("'")])

    def gen_frames(self, video_capture):  
        while not self.stopped:
            print("[INFO] Serving video feed...")
            if video_capture.grabbed:
                frame = video_capture.frame # obtenim el frame de la camera


                if self.type_detector != "None":
                    frame = self.people_detector.scan_people(frame)

                frame = self.vid_fps.put_iterations_per_sec(frame) # mostrem el frame processat

                self.frame = frame # guardem el frame processat a la sortida de video

                print("[INFO] FPS: {}".format(self.vid_fps.countsPerSec()))
                cpu = CPUTemperature()
                print(cpu.temperature)

                # print(str(self.get_cpu_temperature()))
                ret, buffer = cv2.imencode('.jpg', self.frame)
                frame = buffer.tobytes()
                
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

                self.vid_fps.increment()
            else:
                frame = None
                print("[INFO] No frame to show")
            
            
    # def show(self):
    #     while not self.stopped:
    #         ret, buffer = cv2.imencode('.jpg', self.frame)
    #         frame = buffer.tobytes()
    #         yield (b'--frame\r\n'
    #                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

    def stop(self):
        self.stopped = True

        if self.on_finish is not None:
            self.on_finish()