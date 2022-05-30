#######################################################
# Thermal camera Plotter with AMG8833 Infrared Array
#
# by Joshua Hrisko
#    Copyright 2021 | Maker Portal LLC
#
#######################################################
#
import time,sys
sys.path.append('../')
# load AMG8833 module
import amg8833_i2c
import numpy as np
import matplotlib.pyplot as plt
from threading import Thread

#
#####################################
# Initialization of Sensor
#####################################
#

class TermalCameraInput(VideoBaseModule):
    def __init__(self) -> None:
        if hasattr(self, 'th') and self.th.is_alive() or hasattr(self, 'stream') and self.stream.isOpened():
            print("[INFO] Video stream thread already started")
            # self.stop()

        super().__init__()

        self.frame = None

        self.grabbed = True # set to true to start grabbing
        self.stopped = False # set to true to stop grabbing

        t0 = time.time()
        sensor = []
        while (time.time()-t0)<1: # wait 1sec for sensor to start
            try:
                # AD0 = GND, addr = 0x68 | AD0 = 5V, addr = 0x69
                sensor = amg8833_i2c.AMG8833(addr=0x69) # start AMG8833
            except:
                sensor = amg8833_i2c.AMG8833(addr=0x68)
            finally:
                pass
        time.sleep(0.1) # wait for sensor to settle

        # If no device is found, exit the script
        if sensor==[]:
            print("No AMG8833 Found - Check Your Wiring")
            sys.exit(); # exit the app if AMG88xx is not found 

    def join(self):
        self.th.join()

    def start(self):
        print("[INFO] Starting video stream thread...")
        self.th = Thread(target=self.get, args=())
        self.th.daemon = True
        self.th.start()

        if self.on_start is not None:
            self.on_start()
        return self

    def start_figure(self):
        #
        #####################################
        # Start and Format Figure 
        #####################################
        #
        plt.rcParams.update({'font.size':16})
        fig_dims = (12,9) # figure size
        self.fig, self.ax = plt.subplots(figsize=fig_dims) # start figure
        pix_res = (8,8) # pixel resolution
        zz = np.zeros(pix_res) # set array with zeros first
        self.im1 = self.ax.imshow(zz,vmin=15,vmax=40) # plot image, with temperature bounds
        cbar = self.fig.colorbar(self.im1,fraction=0.0475,pad=0.03) # colorbar
        cbar.set_label('Temperature [C]',labelpad=10) # temp. label
        self.fig.canvas.draw() # draw figure

        self.ax_bgnd = self.fig.canvas.copy_from_bbox(self.ax.bbox) # background for speeding up runs
        self.fig.show() # show figure
        
    def plot_loop(self):
        self.start_figure()
        
        #
        #####################################
        # Plot AMG8833 temps in real-time
        #####################################
        #
        pix_to_read = 64 # read all 64 pixels
        while True:
            status,pixels = self.sensor.read_temp(pix_to_read) # read pixels with status
            if status: # if error in pixel, re-enter loop and try again
                continue
            
            T_thermistor = self.sensor.read_thermistor() # read thermistor temp
            self.fig.canvas.restore_region(self.ax_bgnd) # restore background (speeds up run)
            self.im1.set_data(np.reshape(pixels, self.pix_res)) # update plot with new temps
            self.ax.draw_artist(self.im1) # draw image again
            self.fig.canvas.blit(self.ax.bbox) # blitting - for speeding up run
            self.fig.canvas.flush_events() # for real-time plot
            print("Thermistor Temperature: {0:2.2f}".format(T_thermistor)) # print thermistor temp

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
                status, pixels = self.sensor.read_temp(pix_to_read) # read pixels with status
                
                if status: # if error in pixel, re-enter loop and try again
                    self.grabbed = False
                    continue
                
                T_thermistor = self.sensor.read_thermistor() 
                self.frame = np.reshape(pixels, self.pix_res)

                print("Thermistor Temperature: {0:2.2f}".format(T_thermistor)) # print thermistor temp

    def stop(self):
        self.stopped = True
        self.grabbed = False
        self.called = False
        self.sensor.close()
        