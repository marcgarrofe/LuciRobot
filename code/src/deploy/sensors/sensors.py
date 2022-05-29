import serial
import json 
import os
from paho.mqtt import client as mqtt_client

class Sensors:
    def __init__(self, port='/dev/ttyACM0', baudrate=9600, use_mqtt = False, broker = 'localhost', port_mqtt = 1883):

        self.use_mqtt = use_mqtt
        # We read the sensors from the arduino serial port or the mqtt broker
        if not use_mqtt:
            self.ser = serial.Serial(port, baudrate, timeout=0)
        else:
            self.broker = broker 
            self.port = port_mqtt
            self.topic = "/luci/sensors"

            self.mqtt_client = mqtt_client.Client()


        # ho tenim com objecte per si volem accedir desde python pero per el websocket enviare el json
        self.gas_concentration = 0.0
        self.ultrasound_sensor_1_distance = 0.0
        self.ultrasound_sensor_2_distance = 0.0
        self.dht11_humidity = 0.0
        self.dht11_temp = 0.0

        self.json_value = ""
        # self.ser.reset_input_buffer()
    
    def on_message(self, client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        if msg.topic == self.topic:
            self.json_value = msg.payload.decode()
            self.save_to_json(msg.payload.decode())

    """
    Es subscribe a luci/sensors i rep els valors dels sensors 
    """
    def subscribe(self, client: mqtt_client):
        client.subscribe(self.topic)

    """
    Es conecta al raspberry per mqtt per rebre els valors dels sensors
    """
    def connect_mqtt(self) -> mqtt_client:
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
                self.subscribe(self.mqtt_client)
            else:
                print("Failed to connect, return code %d\n", rc)

        self.mqtt_client.on_connect = on_connect
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.connect(self.broker, self.port)

        print ('Starting the MQ loop..')
        self.mqtt_client.loop_start()

    def save_to_json(self, json_text):
        path = os.path.join(self.app.root_path, 'static/sensors.json')
        with open(path, 'w') as outfile:
            json.dump(json_text, outfile)

    def parse_sensors(self, json_text):
        print("Parsing: " + str(json_text))
        print(len(json_text))

        if len(json_text) < 50:
            print("Error parsing json")
            self.json_value = self.error_data()
            return self.json_value

        try: 
            json_dict = json.loads(json_text)

            self.gas_concentration = json_dict['gas_concentration']
            self.ultrasound_sensor_1_distance = json_dict['ultrasound_sensor_1_distance']
            self.ultrasound_sensor_2_distance = json_dict['ultrasound_sensor_2_distance']
            self.dht11_humidity = json_dict['dht11_humidity']
            self.dht11_temp = json_dict['dht11_temp']
            self.json_value = json_dict
        except Exception as e:
            print(e)
            print("Error parsing json")
            self.json_value = self.error_data()
            return self.json_value

        # save json to static flask folder for web app
        path = os.path.join(self.app.root_path, 'static/sensors.json')

        print(path)
        with open(path, 'w') as outfile:
            json.dump(json_text, outfile)

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

    def start_reading(self, app):
        if self.use_mqtt:
            self.connect_mqtt()
            self.app = app


    def read_sensors(self):
        #if self.ser.in_waiting > 0:
        if not self.use_mqtt:
            json_text = self.ser.readline().decode('utf-8')
            print(json_text)
        # if json_text is None or len(json_text) < 1:
        #     return self.parse_sensors(self.error_data())
            
            return self.parse_sensors(json_text)
        else:
            return self.json_value

        #else:
        #    print("No data available from arduino yet.")
        #     return self.parse_sensors(self.error_data())
    
    def get_sensor_values(self):
        return self.json_value
    
    def close(self):
        if self.use_mqtt:
            self.mqtt_client.loop_stop()
            self.mqtt_client.disconnect()
        else:
            self.ser.close()
    
