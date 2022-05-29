#!/usr/bin/env python

#from src.computer_vision.video_stabilization.video_stabilization import video
from src.deploy.server.server import *
from src.deploy.sensors.sensors  import Sensors


from src.deploy.video.video_input import *
from src.deploy.video.video_output import *


def on_start():
    print("[INFO] on_start video capture")

    return

def on_finish():
    print("[INFO] on_finish video capture")
    # Release the video capture object
    video_capture.stop()
    cv2.destroyAllWindows()

    return


"""
Si la idea es que tot funcioni en el pc del client potser no fan falta threads per accedir a les imatges de la càmera

"""
use_threads = True

"""
Aixó es per probar que el client del pc rebi les dades de les sensors del robot raspberry a distancia
"""
use_mqtt = True

# Tenim 4 threads
# - Un per captura de video de webcam
# - Un per captura de video de Raspberry Pi
# - Un per mostrar el video de la webcam
# - Un per mostrar el video de la Raspberry Pi

# Create a video capture object
# video_capture_pi_camera =  VideoInput('picamera', width=320, height=240, use_sockets=True, use_threads=use_threads) # Inicialitza el video input
# video_capture_pi_camera.on_start = on_start # Assigna la funcio on_start al event on_start
# video_capture_pi_camera.on_finish = on_finish # Assigna la funcio on_finish al event on_finish

width = 694
height = 694


video_capture =  VideoInput(1,  width=width, height=height, use_sockets=True, open_port='tcp://192.168.1.44:4445', use_threads=use_threads) # Inicialitza el video input
video_capture.on_start = on_start # Assigna la funcio on_start al event on_start
video_capture.on_finish = on_finish # Assigna la funcio on_finish al event on_finish


# Creo 2 video outputs perque els videos s'han de mostrar en 2 pantalles diferents i si nomes hi ha un 
# thread de output  es maten entre elles XD

video_output = VideoOutput(video_capture.frame, name = 'Hyper rapido', type_detector="None", use_threads=use_threads, use_sockets=False) # inicialitzem la sortida de video
# video_output.on_start = None # assignem el metode on_start que es cridara al iniciar la sortida de video
# video_output.on_finish = on_finish # assignem el metode on_finish a la classe VideoOutput per a que es cridi quan acabi el video o cliquem la lletra q

# video_output_pi = VideoOutput(video_capture.frame, name = 'Hyper rapido', type_detector="None", use_threads=use_threads) # inicialitzem la sortida de video
# video_output_pi.on_start = None # assignem el metode on_start que es cridara al iniciar la sortida de video
# video_output_pi.on_finish = on_finish # assignem el metode on_finish a la classe VideoOutput per a que es cridi quan acabi el video o cliquem la lletra q

# wait for user to press a key to exit
# sensors = None
sensors = Sensors(use_mqtt=use_mqtt, broker='192.168.1.44') # inicialitzem els sensors
server = Server(sensors, video_capture, video_output) # inicialitzem el servidor


video_capture.start() # inicialitzem la captura de video de la camera
# video_capture_pi_camera.start()
video_output.start() # inicialitzem la sortida de video

# sensors.start_reading()
server.start()

if use_threads:
    video_capture.join() # espera que acabi la captura de video de la camera 
 
