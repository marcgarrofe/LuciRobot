from distutils.log import debug
from flask import Flask, g, request, jsonify, render_template, Response, make_response
from flask_socketio import emit
from flask_socketio import SocketIO
from threading import Thread


#from sympy import threaded
# Bibliografía.
# https://stackoverflow.com/questions/51970072/real-time-video-stabilization-opencv

app = Flask(__name__, template_folder = "templates")

app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

sensors = None
video_output = None
video_capture = None
termal_video_input = None

pi_video_capture = None
video_output_pi = None
vid_fps = None

class Server:
    def __init__(self, sensors, video_capture, video_output, termal_video_input, pi_video_capture = None, video_output_pi = None, port=5000, read_sensors = False):
        self.port = port
        self.sensors = sensors

        """
        RGB CAMERA INPUT 
        """
        self.video_output = video_output
        self.video_capture = video_capture

        """
        TERMAL CAMERA   
        """
        self.termal_video_input = termal_video_input

        """
        PI CAMERA INPUT (not in use)
        """
        self.video_output_pi = video_output_pi
        self.pi_video_capture = pi_video_capture

        self.vid_fps = vid_fps
        self.read_sensors = read_sensors

    def start(self):
        print("[INFO] Starting server...")
        # app.run(port=self.port, debug=True)
        global sensors
        global video_output

        global termal_video_input
        global pi_video_capture
        global video_capture
        global video_output_pi

        sensors = self.sensors
        video_output = self.video_output
        pi_video_capture = self.pi_video_capture
        video_capture = self.video_capture
        video_output_pi = self.video_output_pi
        termal_video_input = self.termal_video_input

        self.start_server()

    def start_server(self): 
        socketio.run(app, host='0.0.0.0', port = self.port, debug=True, use_reloader  = False)
        
    def start_thread(self):
        thread = Thread(target=self.start_server)
        thread.start()




@socketio.on("get_sensors")
def get_sensors(data):
    try: 
        sensor_data = sensors.read_sensors()
        print("Serial received: " + str(sensor_data))
        emit('receive_sensors', sensor_data)
    except Exception as e:
        print(str(e))
        emit('receive_sensors', str(e))

@socketio.on("on_client")
def on_client(data):
    print(data)

    if 'data' in data:
        print(data)
        message = data['data']

        if message == "disconnected":
            print("[INFO] Client disconnected")
            video_capture.stop()
            video_output.stop()

        elif message == "connected":
            print("[INFO] Client connected")


@app.route('/')
def home():
    # show the index.html page
    return  render_template("index.html")

@app.route('/video_feed')
def video_feed():
    return Response(video_output.gen_frames(video_capture, termal_video_input), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/picamera_video_feed')
def picamera_video_feed():
    return Response(video_output_pi.gen_frames(pi_video_capture), mimetype='multipart/x-mixed-replace; boundary=frame')
