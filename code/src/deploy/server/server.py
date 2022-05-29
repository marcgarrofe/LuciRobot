from distutils.log import debug

from flask import Flask, g, request, jsonify, render_template, Response, make_response
from flask_socketio import emit
from flask_socketio import SocketIO
# from flask_mqtt import Mqtt

from threading import Thread
import paho.mqtt.client as mqtt

import os
import json

# import eventlet

# eventlet.monkey_patch()

#from sympy import threaded
# Bibliografía.
# https://stackoverflow.com/questions/51970072/real-time-video-stabilization-opencv

app = Flask(__name__, template_folder = "templates")
app.config['SECRET_KEY'] = 'secret!'

# app.config['TEMPLATES_AUTO_RELOAD'] = True
# app.config['MQTT_BROKER_URL'] = '192.168.1.44'
# app.config['MQTT_BROKER_PORT'] = 1883
# app.config['MQTT_USERNAME'] = ''
# app.config['MQTT_PASSWORD'] = ''
# app.config['MQTT_KEEPALIVE'] = 5
# app.config['MQTT_TLS_ENABLED'] = False


# mqtt = Mqtt(app)
# # mqtt.subscribe('luci/sensors')

# socketio = SocketIO(app, async_mode='gevent', cors_allowed_origins="*")
socketio = SocketIO(app)

client = mqtt.Client()
sensors = None
video_output = None
video_capture = None
pi_video_capture = None
video_output_pi = None
vid_fps = None

class Server:
    def __init__(self, sensors, video_capture, video_output, pi_video_capture = None, video_output_pi = None, port=5000, read_sensors = False):
        self.port = port
        self.sensors = sensors

        self.video_output = video_output

        self.video_capture = video_capture
        self.video_output_pi = video_output_pi
        self.pi_video_capture = pi_video_capture

        self.vid_fps = vid_fps
        self.read_sensors = read_sensors

    def start(self):
        print("[INFO] Starting server...")
        # app.run(port=self.port, debug=True)
        global sensors
        global video_output
        global pi_video_capture
        global video_capture
        global video_output_pi

        sensors = self.sensors
        video_output = self.video_output
        pi_video_capture = self.pi_video_capture
        video_capture = self.video_capture
        video_output_pi = self.video_output_pi

        self.start_server()

    def start_server(self): 
        # self.start_mqtt()
        self.sensors.start_reading(app)

        socketio.run(app, host='0.0.0.0', port = self.port, debug=True, use_reloader  = False)
        
    # def start_mqtt(self,):
    #     global client
        
    #     client.on_connect = on_connect
    #     client.on_message = on_message
    #     client.connect('192.168.1.44', 1883, keepalive=60)

    #     print ('Starting the MQ loop..')
    #     client.loop_start()   


    def start_thread(self):
        thread = Thread(target=self.start_server)
        thread.start()

    

@app.route('/')
def home():
    # show the index.html page
    return  render_template("index.html")

@app.route('/video_feed')
def video_feed():
    return Response(video_output.gen_frames(video_capture), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/picamera_video_feed')
def picamera_video_feed():
    return Response(video_output_pi.gen_frames(pi_video_capture), mimetype='multipart/x-mixed-replace; boundary=frame')


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
    # global sensors

    print(data)
    message = data['data']
    
    if message == "disconnected":
        print("[INFO] Client disconnected")
        video_capture.stop()
        video_output.stop()
        
        # sensors.close()

    elif message == "connected":
        print("[INFO] Client connected")
        

# MQTT

# def on_connect (client, userdata, flags, rc):
#     print('* Connected to MQTT broker *')
#     client.subscribe ('/luci/sensors', qos=0)

# def on_message (client, userdata, msg):
#     print('* Message received from MQTT broker *')
#     print(msg.topic + " " + str(msg.payload.decode()))
#     # with app.app_context():
#     #     socketio.emit('receive_sensors', msg.payload.decode())
#     # save to json on static folder
#     path = os.path.join(app.root_path, 'static/sensors.json')
#     print(path)
#     with open(path, 'w') as outfile:
#         json.dump(msg.payload.decode(), outfile)
#     # emit('receive_sensors', msg.payload.decode())



# @mqtt.on_connect()
# def handle_connect(client, userdata, flags, rc):
#     print("[INFO] Connected to MQTT broker")
#     mqtt.subscribe("/luci/sensors")

# @mqtt.on_subscribe()
# def handle_subscribe(client, userdata, mid, granted_qos):
#     print('Subscription id {} granted with qos {}.'.format(mid, granted_qos))

# @mqtt.on_message()
# def handle_mqtt_message(client, userdata, message):
#     print("[MQTT] Received message: " + str(message.payload.decode()))
#     socketio.emit('receive_sensors', data=message.payload.decode())

# @mqtt.on_log()
# def handle_logging(client, userdata, level, buf):
#     print(level, buf)