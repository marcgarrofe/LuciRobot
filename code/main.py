# from src.computer_vision.video_stabilization.video_stabilization import video
from src.deploy.server.server import *
from src.deploy.sensors.sensors  import Sensors

from src.deploy.video.video_fps import *
from src.deploy.video.video_input import *
from src.deploy.video.video_output import *


def on_start():
    print("[INFO] Started video capture")
    return

def on_finish():
    print("[INFO] Finished video capture")
    # Release the video capture object
    vid_capture.stop()
    cv2.destroyAllWindows()

    return

vid_capture =  VideoInput(0,  width=640, height=480) # Inicialitza el video input
vid_capture.on_start = on_start
vid_capture.start() # inicialitzem la captura de video de la camera

vid_fps = VideoFPS().start() # inicialitzem els frames per segon

vid_output = VideoOutput(vid_capture.frame, name = 'Hyper rapido') # inicialitzem la sortida de video
vid_output.on_start = None # assignem el metode on_finish a la classe VideoOutput per a que es cridi quan acabi el video o cliquem la lletra q
vid_output.on_finish = on_finish # assignem el metode on_finish a la classe VideoOutput per a que es cridi quan acabi el video o cliquem la lletra q

sensors = Sensors()

server = Server(sensors, vid_output)
server.start_server()

while True:
    if vid_capture.stopped or vid_output.stopped:
        vid_capture.stop()
        vid_output.stop()
        break

    frame = vid_capture.frame # obtenim el frame de la camera
    
    # frame = stabilizer.process_frame(frame) # processem el frame. AQUI ES CRIDA AL NOSTRE CODI QUE JUNTA LES IMATYGES O ESTABLITZA O WHATEVER
 
    frame = vid_fps.put_iterations_per_sec(frame) # mostrem el frame processat
    
    vid_output.frame = frame # guardem el frame processat

    vid_fps.increment()

# Els sensors es llegiran a petició del websocket en el client web (index.html)