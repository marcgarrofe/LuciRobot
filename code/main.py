#!/usr/bin/env python

#from src.computer_vision.video_stabilization.video_stabilization import video
from src.deploy.server.server import *
from src.deploy.sensors.sensors  import Sensors


from src.deploy.video.video_input import *
from src.deploy.video.video_output import *

from src.voice.voice import *

def on_start():
    print("[INFO] on_start video capture")

    return

def on_finish():
    print("[INFO] on_finish video capture")
    # Release the video capture object
    video_capture.stop()
    cv2.destroyAllWindows()

    return

# Tenim 4 threads
# - Un per captura de video de webcam
# - Un per captura de video de Raspberry Pi
# - Un per mostrar el video de la webcam
# - Un per mostrar el video de la Raspberry Pi

# Create a video capture object
# video_capture_pi_camera =  VideoInput('picamera', width=320, height=240) # Inicialitza el video input
# video_capture_pi_camera.on_start = on_start # Assigna la funcio on_start al event on_start
# video_capture_pi_camera.on_finish = on_finish # Assigna la funcio on_finish al event on_finish


video_capture =  VideoInput(1,  width=320, height=240) # Inicialitza el video input
video_capture.on_start = on_start # Assigna la funcio on_start al event on_start
video_capture.on_finish = on_finish # Assigna la funcio on_finish al event on_finish


# Creo 2 video outputs perque els videos s'han de mostrar en 2 pantalles diferents i si nomes hi ha un 
# thread de output  es maten entre elles XD

video_output = VideoOutput(video_capture.frame, name = 'Hyper rapido', type_detector="None") # inicialitzem la sortida de video
video_output.on_start = None # assignem el metode on_start que es cridara al iniciar la sortida de video
video_output.on_finish = on_finish # assignem el metode on_finish a la classe VideoOutput per a que es cridi quan acabi el video o cliquem la lletra q

# video_output_pi = VideoOutput(video_capture.frame, name = 'Hyper rapido', type_detector="None") # inicialitzem la sortida de video
# video_output_pi.on_start = None # assignem el metode on_start que es cridara al iniciar la sortida de video
# video_output_pi.on_finish = on_finish # assignem el metode on_finish a la classe VideoOutput per a que es cridi quan acabi el video o cliquem la lletra q


sensors = Sensors() # inicialitzem els sensors
server = Server(sensors, video_capture,  video_output) # inicialitzem el servidor

save_location = os.path.join(app.root_path, '/static/voice_response.json')
voice_input = VoiceInput(lang_code="es-ES", save_location = save_location)


video_capture.start() # inicialitzem la captura de video de la camera
video_output.start() # inicialitzem la sortida de video

voice_input.start()
sensors.start_reading()
server.start()

video_capture.join() # espera que acabi la captura de video de la camera 
 
