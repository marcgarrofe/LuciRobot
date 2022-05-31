# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""This example is for Raspberry Pi (Linux) only!
   It will not work on microcontrollers running CircuitPython!"""

import os
import math
import time

import numpy as np

from scipy.interpolate import griddata

from colour import Color

from src.deploy.video.thermal.amg8833_i2c import AMG8833


from threading import Thread
import cv2
from src.deploy.video.video_module_base import VideoBaseModule
#
#####################################
# Initialization of Sensor
#####################################
#

# low range of the sensor (this will be blue on the screen)
MINTEMP = 26.0

# high range of the sensor (this will be red on the screen)
MAXTEMP = 32.0

# how many color values we can have
COLORDEPTH = 1024


class TermalCameraInput(VideoBaseModule):
    def __init__(self, width = 640, height = 480) -> None:
        if hasattr(self, 'th') and self.th.is_alive() or hasattr(self, 'stream') and self.stream.isOpened():
            print("[INFO] Video stream thread already started")
            # self.stop()

        super().__init__()

        self.frame = None

        self.grabbed = True # set to true to start grabbing
        self.stopped = False # set to true to stop grabbing


        # initialize the sensor
        self.init_sensor()

        self.points = [(math.floor(ix / 8), (ix % 8)) for ix in range(0, 64)]

        self.grid_x, self.grid_y = np.mgrid[0:7:32j, 0:7:32j]

        # sensor is an 8x8 grid so lets do a square
        self.height = height
        self.width = width

        # the list of colors we can choose from
        blue = Color("indigo")
        colors = list(blue.range_to(Color("red"), COLORDEPTH))

        # create the array of colors
        self.colors = [(int(c.red * 255), int(c.green * 255), int(c.blue * 255)) for c in colors]

        pixelSize = 30

        self.displayPixelWidth = self.width / pixelSize
        self.displayPixelHeight = self.height / pixelSize

    def init_sensor(self):
        t0 = time.time()
        self.sensor = []
        while (time.time()-t0)<1: # wait 1sec for sensor to start
            try:
                # AD0 = GND, addr = 0x68 | AD0 = 5V, addr = 0x69
                self.sensor = AMG8833(addr=0x69) # start AMG8833
            except:
                self.sensor = AMG8833(addr=0x68)
            finally:
                pass
        time.sleep(0.1) # wait for sensor to settle

        # If no device is found, exit the script
        if self.sensor==[]:
            print("No AMG8833 Found - Check Your Wiring")
            sys.exit(); # exit the app if AMG88xx is not found 

    # some utility functions
    def constrain(self, val, min_val, max_val):
        return min(max_val, max(min_val, val))


    def map_value(self, x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    
    def join(self):
        self.th.join()

    def start(self):
        print("[INFO] Starting video stream thread...")
        self.th = Thread(target=self.get, args=())
        self.th.daemon = True
        self.th.start()

        super().start()

    """
    Get the current frame from the thermal camera
    """    
    def get(self):

        pix_to_read = 64 # read all 64 pixels

        while not self.stopped:
            if not self.grabbed:
                print("Error thermal camera")
                self.stop()
            else:
                # read the pixels
                # pixels = []
                
                status, pixels = self.sensor.read_temp(pix_to_read) # read pixels with status
                
                if status: # if error in pixel, re-enter loop and try again
                    print ("Error reading pixels")
                    continue

                pixels = [self.map_value(p, MINTEMP, MAXTEMP, 0, COLORDEPTH - 1) for p in pixels]

                # perform interpolation
                bicubic = griddata(self.points, pixels, (self.grid_x, self.grid_y), method="cubic")

                # create empty frame
                self.frame = np.zeros((self.height, self.width, 3), np.uint8)

                # print(len(bicubic))

                for ix, row in enumerate(bicubic):
                    # print(len(row))
                    for jx, pixel in enumerate(row):

                        c = self.colors[self.constrain(int(pixel), 0, COLORDEPTH - 1)]

                        self.frame[int(self.displayPixelHeight * ix):int(self.displayPixelHeight * (ix + 1)), int(self.displayPixelWidth * jx):int(self.displayPixelWidth * (jx + 1))] = c

                self.frame = np.fliplr(self.frame)

    def stop(self):
        self.grabbed = False
        super().stop()
        