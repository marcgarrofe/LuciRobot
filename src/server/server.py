from flask import Flask, request, jsonify, render_template
from flask_socketio import emit
from flask_socketio import SocketIO

# Bibliografía.
# https://stackoverflow.com/questions/51970072/real-time-video-stabilization-opencv

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
sensors = None

class server:
    def __init__(self, port=5000, sensors=None):
        self.port = port
        self.sensors = sensors
        

    def start_server(self):
        # app.run(port=self.port, debug=True)
        global sensors
        sensors = self.sensors
        socketio.run(app, port = self.port, debug=True)


@socketio.on("get_sensors")
def get_sensors(data):
    try: 
        emit('get_sensors', sensors.read_sensors())
    except Exception as e:
        print(str(e))
        emit('get_sensors', str(e))

@socketio.on("on_client")
def on_client(data):
    print(data)

@app.route('/')
# route function
def home():
    # show the index.html page
    return  render_template("index.html")


