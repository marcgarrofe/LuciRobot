import cv2
from src.computer_vision.object_detector.hog_detector import people_detectorHOG
from src.computer_vision.video_stabilization.video_stabilization import StabilizerHomography
from src.computer_vision.object_detector.ssd_detector import people_detectorSSD


DETECTOR = 'SSD'            # POT SER "SSD" o "HOG"
STABILIZER = 'VIDSTAB'      # POT SER "homography" o "vidstab"


video_options = {
    "CAP_PROP_FRAME_WIDTH": 640,
    "CAP_PROP_FRAME_HEIGHT": 480,
    "CAP_PROP_FPS": 10,
}

if DETECTOR == 'SSD':
    detector = people_detectorSSD()
elif DETECTOR == 'HOG':
    detector = people_detectorHOG()
else:
    raise ValueError("No Detector selected")

stabilizer = StabilizerHomography(type=STABILIZER, resize=True, crop_frame=True, compare_stabilization=False, buffer_size=5)
err, frame = stabilizer.get_stabilized_frame()

# Declarem loop infinit
while err is True:
    cv2.imshow("video", frame)
    key = cv2.waitKey(20)
    if key == ord('q'):
        break
    err, frame = stabilizer.get_stabilized_frame()
    frame = detector.scan_people(frame)