import cv2
import numpy as np

# Bibliografia : https://learnopencv.com/video-stabilization-using-point-feature-matching-in-opencv/

class video_stabilizer:
    # def __init__(self):

    def stabilize_frame(self, frame):
        # Detect feature points in previous frame
        prev_pts = cv2.goodFeaturesToTrack(frame,
                                           maxCorners=200,
                                           qualityLevel=0.01,
                                           minDistance=30,
                                           blockSize=3)
        return prev_pts


"""
goodFeaturesToTrack -> Fa 10 anys
SIFT -> Punts de control
Mirar IBM - Hiperlapse (Reconstruccio 3d de l'escena)
Deep-learning amb SIFT (D2? ORB SLAM? )

"""