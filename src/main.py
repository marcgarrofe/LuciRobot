
import cv2
from src.computer_vision.object_detector.object_detector import people_detectorHOG
from src.computer_vision.video_stabilization.video_stabilization import Stabilizer

video_options = {
    "CAP_PROP_FRAME_WIDTH": 640,
    "CAP_PROP_FRAME_HEIGHT": 480,
    "CAP_PROP_FPS": 10,
}

stabilizer = Stabilizer(resize=True, crop_frame=True, compare_stabilization=False, buffer_size=5)
detector = people_detectorHOG()

err, frame = stabilizer.get_stabilized_frame_kp()

# Declarem loop infinit
while err is True:
    cv2.imshow("video", frame)
    key = cv2.waitKey(20)
    if key == ord('q'):
        break
    err, frame = stabilizer.get_stabilized_frame_kp()
    frame = detector.scan_people(frame)