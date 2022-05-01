# from src.computer_vision.video_stabilization.video_stabilization import video
from src.deploy.server.server import *
from src.deploy.sensors.sensors  import Sensors

# video = video(stabilize=True)

sensors = Sensors(port='COM5')

server = Server(sensors)
server.start_server()

# Declarem loop infinit
# while True:
#     frame = video.get_frame()
#     video.show_frame(frame)

    # Els sensors es llegiran a petició del websocket en el client web (index.html)