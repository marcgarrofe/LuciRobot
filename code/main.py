# from src.computer_vision.video_stabilization.video_stabilization import video
from src.deploy.server.server import *
from src.deploy.sensors.sensors  import Sensors

from src.deploy.video.video_fps import *
from src.deploy.video.video_input import *
from src.deploy.video.video_output import *


def on_start():
    print("[INFO] on_start video capture")

    return

def on_finish():
    print("[INFO] on_finish video capture")
    # Release the video capture object
    vid_capture.stop()
    cv2.destroyAllWindows()

    return

vid_capture =  VideoInput(0,  width=640, height=480) # Inicialitza el video input
vid_capture.on_start = on_start # Assigna la funcio on_start al event on_start
vid_capture.on_finish = on_finish # Assigna la funcio on_finish al event on_finish

vid_fps = VideoFPS().start() # inicialitzem el sistema que calcula els frames per segon

vid_output = VideoOutput(vid_capture.frame, name = 'Hyper rapido') # inicialitzem la sortida de video
vid_output.on_start = None # assignem el metode on_start que es cridara al iniciar la sortida de video
vid_output.on_finish = on_finish # assignem el metode on_finish a la classe VideoOutput per a que es cridi quan acabi el video o cliquem la lletra q

sensors = Sensors()
server = Server(sensors, vid_capture,  vid_output, vid_fps)

vid_capture.start() # inicialitzem la captura de video de la camera
server.start()
vid_capture.join() # espera que acabi la captura de video de la camera 
 