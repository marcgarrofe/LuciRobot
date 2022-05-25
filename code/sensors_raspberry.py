import serial
import json 
from paho.mqtt import client as mqtt_client
import random

# run this program on each RPi to send a labelled image stream
import socket
import time
from imutils.video import VideoStream
import imagezmq

# https://github.com/jeffbass/imagezmq

class SensorsRaspberry:
    def __init__(self, port='/dev/ttyACM0', baudrate=9600, read_sensors = False):
        self.ser = serial.Serial(port, baudrate, timeout=0)

        self.sender = imagezmq.ImageSender(connect_to='tcp://jeff-macbook:5555')

        self.rpi_name = socket.gethostname() # send RPi hostname with each image
        self.picam = VideoStream(usePiCamera=False).start()
        time.sleep(2.0)  # allow camera sensor to warm up

        self.mqtt_client  = mqtt_client.Client()
        self.port = 1883
        self.topic = "/luci/sensors"
        self.client_id = f'python-mqtt-{random.randint(0, 1000)}'

        # ho tenim com objecte per si volem accedir desde python pero per el websocket enviare el json
        self.gas_concentration = 0.0
        self.ultrasound_sensor_1_distance = 0.0
        self.ultrasound_sensor_2_distance = 0.0
        self.dht11_humidity = 0.0
        self.dht11_temp = 0.0
        self.json_value = ""
        # self.ser.reset_input_buffer()
    
    def parse_sensors(self, json_text):
        print("Parsing: " + str(json_text))
        print(len(json_text))
        json_dict = json.loads(json_text)

        self.gas_concentration = json_dict['gas_concentration']
        self.ultrasound_sensor_1_distance = json_dict['ultrasound_sensor_1_distance']
        self.ultrasound_sensor_2_distance = json_dict['ultrasound_sensor_2_distance']
        self.dht11_humidity = json_dict['dht11_humidity']
        self.dht11_temp = json_dict['dht11_temp']
        self.json_value = json_dict

        return json_text

    def error_data(self):
        json_text = {}
        json_text["gas_concentration"] = 0.0
        json_text["ultrasound_sensor_1_distance"] = 0.0
        json_text["ultrasound_sensor_2_distance"] = 0.0
        json_text["dht11_humidity"] = 0.0
        json_text["dht11_temp"] = 0.0
        
        app_json = json.dumps(json_text)

        self.json_value = app_json

        return str(app_json)

    """
    Starts emitting sensor data to the client by MQTT and images by sockets.
    """
    def start_emiting(self):
        print("Starting emiting")
        while True:
            self.read_sensors()

            image = self.picam.read()
            self.sender.send_image(self.rpi_name, image)


    def read_sensors(self):
        #if self.ser.in_waiting > 0:
        json_text = self.ser.readline().decode('utf-8')
        print(json_text)
        result = self.mqtt_client.publish(self.topic, json_text)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{json_text}` to topic `{self.topic}`")
        else:
            print(f"Failed to send message to topic {self.topic}")
        
    def close(self):
        self.ser.close()
    

if __name__ == "__main__":
    # test
    sensors = SensorsRaspberry()
    sensors.start_emiting()