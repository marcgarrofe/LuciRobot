from vidgear.gears import VideoGear
import cv2


# Bibliografía.
# https://stackoverflow.com/questions/51970072/real-time-video-stabilization-opencv


class video:
    def __init__(self, stabilize=True):
        # To open any valid video stream(for e.g device at 0 index)
        self.stream = VideoGear(source=0, stabilize=stabilize).start()

    def get_frame(self):
        frame = self.stream.read()
        if frame is None:
            raise Exception("Frame Error")
            self.end_stream()
        return frame

    def show_frame(self, frame):
        cv2.imshow("Stabilized Frame", frame)
        cv2.waitKey(1)

    def end_stream(self):
        cv2.destroyAllWindows()  # Close output window
        self.stream.stop()  # Safely close video stream
