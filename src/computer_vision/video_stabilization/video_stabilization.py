import numpy as np
import cv2


default_options = {
    'width' : 480,
    'height' : 320
}

def calculate_weights(number_frames, divide_by=2):
    list_weights = list()
    last_weight = 1.0
    for i in range(number_frames):
        weight = last_weight / divide_by
        list_weights.append(weight)
        last_weight = weight
    return list_weights


def crop_frame(frame, proportion):
    width = frame.shape[1]
    height = frame.shape[0]

    x_crop = int(width * proportion / 2)
    y_crop = int(height * proportion / 2)

    frame = frame[y_crop:height-y_crop, x_crop:width-x_crop]

    return cv2.resize(frame, dsize=(width, height))


class Stabilizer:
    def __init__(self, video_path=None, camera_source=0, gray_scale=False, resize=False, crop_frame=True, compare_stabilization=False, buffer_size=5):

        # Identifiquem si el input del estabilitzador és un video o una camera
        if video_path is not None:
            self.video_path = video_path
        else:
            self.camera_source = camera_source

        self.gray_scale = gray_scale
        self.resize = resize
        self.crop_frame = crop_frame
        self.compare_stabilization = compare_stabilization

        self.orb = cv2.ORB_create(nfeatures=1000)

        if video_path is not None:
            self.vid_capture = cv2.VideoCapture(video_path)
        else:
            self.vid_capture = cv2.VideoCapture(self.camera_source)

        if self.vid_capture.isOpened() is False:
            raise ValueError("Error opening the video file")

        if resize is False:
            self.width = int(self.vid_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
            self.height = int(self.vid_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        else:
            self.width = default_options['width']
            self.height = default_options['height']

        # Obtenim el primer frame
        err, self.previous_frame = self.get_frame()

        if err is False:
            raise ValueError("Error getting first frame")

        self.homography_buffer_size = buffer_size
        self.list_weights = calculate_weights(self.homography_buffer_size, divide_by=0.7)
        self.homography_buffer = list()

        if self.gray_scale is True:
            self.previous_frame_gray = self.previous_frame
        else:
            self.previous_frame_gray = cv2.cvtColor(self.previous_frame, cv2.COLOR_BGR2GRAY)

        # Calculem punts de referència i descriptors amb el detector ORB
        self.prev_keypoints, self.prev_descriptors = self.orb.detectAndCompute(self.previous_frame, None)


    def get_frame(self):
        if self.vid_capture.isOpened() is False:
            raise ValueError("Video Stream is not opened")
        err, frame = self.vid_capture.read()

        if err is False:
            return False, None

        if self.gray_scale is True:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if self.resize is True:
            frame = cv2.resize(frame, (self.width, self.height))

        return err, frame

    def get_stabilized_frame_kp(self):
        # Obtenim frame
        err, frame = self.get_frame()

        if err is False:
            return err, None

        if self.compare_stabilization:
            original_frame = frame

        # Calculem punts de referència i descriptors amb el detector ORB
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        keypoints, descriptors = self.orb.detectAndCompute(gray_frame, None)

        # Create a BFMatcher object.
        # It will find all of the matching keypoints on two images
        bf = cv2.BFMatcher_create(cv2.NORM_HAMMING)

        # Find matching points
        matches = bf.knnMatch(self.prev_descriptors, descriptors, k=2)

        # Finding the best matches
        THR = 0.6
        good = []
        for m, n in matches:
            if m.distance < THR * n.distance:
                good.append(m)

        # print("Number ORB Good Points = " + str(len(good)))

        # Set minimum match condition
        MIN_MATCH_COUNT = 6

        if len(good) > MIN_MATCH_COUNT:
            # Convert keypoints to an argument for findHomography
            src_pts = np.float32([ self.prev_keypoints[m.queryIdx].pt for m in good]).reshape(-1,1,2)
            dst_pts = np.float32([ keypoints[m.trainIdx].pt for m in good]).reshape(-1,1,2)

            # Càlcul Homografia automàticament
            H, _ = cv2.findHomography(dst_pts, src_pts, cv2.RANSAC,6.0)

            if len(self.homography_buffer) < self.homography_buffer_size:
                self.homography_buffer.append(H)
            else:
                # Eliminem primer element (el més antic de la llista)
                self.homography_buffer.pop(0)
                # Afegim última homografia
                self.homography_buffer.append(H)

                # Calculem la mitjana
                # H = sum(self.homography_buffer) / len(self.homography_buffer)
                H = np.average(self.homography_buffer, weights=self.list_weights, axis=0)
                # H = np.mean(self.homography_buffer, axis=0)

                # Sobrescrivim la última homogarfia afegida per la mitjana
                self.homography_buffer[-1] = H

            # Apliquem la projecció al frame
            frame = cv2.warpPerspective(frame, H, (frame.shape[1], frame.shape[0]))


            if self.crop_frame is True:
                frame = crop_frame(frame, proportion=0.1)

        self.prev_descriptors = descriptors
        self.prev_keypoints = keypoints
        self.previous_frame = frame

        if self.compare_stabilization:
            # Concatenate stabilizated frame with the original frame
            frame = np.concatenate((frame, crop_frame(original_frame, 0.1)), axis=1)

        return err, frame

