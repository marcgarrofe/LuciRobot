from datetime import datetime
import argparse
import cv2
from threading import Thread

class VideoFPS:
    """
    Class that tracks the number of occurrences ("counts") of an
    arbitrary event and returns the frequency in occurrences
    (counts) per second. The caller must increment the count.
    """

    def __init__(self):
        self._start_time = None
        self._num_occurrences = 0

    def start(self):
        self._start_time = datetime.now()
        return self

    def increment(self):
        self._num_occurrences += 1

    def countsPerSec(self):
        elapsed_time = (datetime.now() - self._start_time).total_seconds()
        return self._num_occurrences / elapsed_time

    def put_iterations_per_sec(self, frame):
        """
        Add iterations per second text to lower-left corner of a frame.
        """

        cv2.putText(frame, "{:.0f} iterations/sec".format(self.countsPerSec()),
            (10, 450), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255))
        return frame