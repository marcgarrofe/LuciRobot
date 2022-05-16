# run this program on the Mac to display image streams from multiple RPis
import cv2
import imagezmq
image_hub = imagezmq.ImageHub()

from src.computer_vision.object_detector.ssd_detector import people_detectorSSD
detector = people_detectorSSD()

while True:  # show streamed images until Ctrl-C
    rpi_name, image = image_hub.recv_image()

    image = detector.scan_people(image)

    cv2.imshow(rpi_name, image) # 1 window for each RPi
    cv2.waitKey(20)
    image_hub.send_reply(b'OK')