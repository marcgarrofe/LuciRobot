import numpy as np
import cv2
from src.computer_vision.object_detector.ssd_detector import people_detectorSSD

SOURCE = 'http://192.168.1.150:5000/video_feed'
SOURCE = 0

detector = people_detectorSSD()

cap = cv2.VideoCapture(SOURCE)
while(cap.isOpened()):
    
    ret, frame = cap.read() 

    if ret:
        frame = detector.scan_people(frame)
        cv2.imshow("Image", frame)
    else:
       print('no video')
       cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
       continue
    
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break
    
    
cap.release()
cv2.destroyAllWindows()
