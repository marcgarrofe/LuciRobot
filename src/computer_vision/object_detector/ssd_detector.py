import numpy as np
import cv2
import os

GPU_SUPPORT = False

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'relative/path/to/file/you/want')

# PROTOTXT = "model/MobileNetSSD_deploy.prototxt"
# MODEL = "model/MobileNetSSD_deploy.caffemodel"

PROTOTXT = os.path.join(dirname, 'model/MobileNetSSD_deploy.prototxt')
MODEL = os.path.join(dirname, 'model/MobileNetSSD_deploy.caffemodel')

"""
BIBLIOGRAFIA :
https://medium.com/featurepreneur/object-detection-using-single-shot-multibox-detection-ssd-and-opencvs-deep-neural-network-dnn-d983e9d52652
"""

class people_detectorSSD():
    def __init__(self):
        self.net = cv2.dnn.readNetFromCaffe(PROTOTXT, MODEL)
        if GPU_SUPPORT:
            self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
            self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

        self.CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat", "bottle", "bus",  "car", "cat", "chair", "cow", "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]
        self.COLORS = np.random.uniform(0, 255, size=(len(self.CLASSES), 3))


    def scan_people(self, frame):
        h, w = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(frame, 0.007843, (300, 300), 127.5)
        self.net.setInput(blob)
        detections = self.net.forward()
        for i in np.arange(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.5:
                idx = int(detections[0, 0, i, 1])
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                label = "{}: {:.2f}%".format(self.CLASSES[idx],confidence*100)
                cv2.rectangle(frame, (startX, startY), (endX, endY),    self.COLORS[idx], 2)
                y = startY - 15 if startY - 15 > 15 else startY + 15
                cv2.putText(frame, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.COLORS[idx], 2)
        return frame