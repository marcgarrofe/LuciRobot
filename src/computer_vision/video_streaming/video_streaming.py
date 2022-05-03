from vidgear.gears import VideoGear
import cv2
from ..object_detector.object_detector import people_detectorHOG
from ..video_stabilization.video_stabilization import video_stabilizer


# Bibliografía.
# https://stackoverflow.com/questions/51970072/real-time-video-stabilization-opencv

default_video_options = {
    "CAP_PROP_FRAME_WIDTH": 320,
    "CAP_PROP_FRAME_HEIGHT": 240,
    "CAP_PROP_FPS": 60,
}


class video:
    def __init__(self, stabilize=False, record=False, detect_people=False, video_options=default_video_options):
        # To open any valid video stream(for e.g device at 0 index)
        self.stream = VideoGear(source=0, stabilize=stabilize).start()

        self.record = record
        self.stabilize = stabilize
        self.detect_people = detect_people

        self.height = video_options["CAP_PROP_FRAME_HEIGHT"]
        self.width = video_options["CAP_PROP_FRAME_WIDTH"]
        self.fps = video_options["CAP_PROP_FPS"]

        if record is True:
            self.out = cv2.VideoWriter(
                'output.avi',
                cv2.VideoWriter_fourcc(*'MJPG'),
                float(self.fps),
                # 60.,
                (self.width, self.height))

        if detect_people is True:
            self.object_detector = people_detectorHOG()

    def get_frame(self):
        frame = self.stream.read()
        if frame is None:
            self.end_stream()
            self.out.release()
            raise Exception("Frame Error")

        if self.detect_people is True:
            frame = self.object_detector.scan_people(frame)

        if self.record is True:
            # Write the output video
            self.out.write(frame.astype('uint8'))

        return frame

    def show_frame(self, frame):
        cv2.imshow("Stabilized Frame", frame)
        cv2.waitKey(1)

    def end_stream(self):
        cv2.destroyAllWindows()  # Close output window
        self.stream.stop()  # Safely close video stream
        self.out.release()


class video_v2:
    def __init__(self, stabilize=False, video_options=default_video_options, gray_scale=True):
        # Streaming options
        self.stabilize = stabilize
        self.gray_scale = gray_scale

        # Video propieties
        self.height = video_options["CAP_PROP_FRAME_HEIGHT"]
        self.width = video_options["CAP_PROP_FRAME_WIDTH"]
        self.fps = video_options["CAP_PROP_FPS"]

        # Start Streaming
        self.stream = cv2.VideoCapture(0)

        # Check if the webcam is opened correctly
        if not self.stream.isOpened():
            raise IOError("Cannot open webcam")

        if self.stabilize is True:
            self.stabilizer = video_stabilizer


    def get_frame(self):
        frame = self.stream.read()[1]

        if frame is None:
            self.end_stream()
            raise Exception("Frame Error")

        if self.gray_scale is True:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        frame = cv2.resize(frame, (self.width, self.height), interpolation = cv2.INTER_LINEAR)

        if self.stabilize is True:
            # frame = self.stabilizer.stabilize_frame(frame)

            prev_pts = cv2.goodFeaturesToTrack(frame,
                                               maxCorners=200,
                                               qualityLevel=0.01,
                                               minDistance=30,
                                               blockSize=3)
        return frame

    def end_stream(self):
        cv2.destroyAllWindows()  # Close output window
        self.stream.stop()  # Safely close video stream

    def show_frame(self, frame):
        cv2.imshow("Luci's cam", frame)
        cv2.waitKey(1)




