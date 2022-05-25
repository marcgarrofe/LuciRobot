import serial
import json 
from paho.mqtt import client as mqtt_client

class Sensors:
    def __init__(self, port='/dev/ttyACM0', baudrate=9600, use_mqtt = False, broker = 'localhost', port_mqtt = 1883):

        self.use_mqtt = use_mqtt
        # We read the sensors from the arduino serial port or the mqtt broker
        if use_mqtt:
            self.ser = serial.Serial(port, baudrate, timeout=0)
        else:
            self.broker = broker 
            self.port = port_mqtt
            self.topic = "/luci/sensors"
            self.mqtt_client.loop_start()

        # ho tenim com objecte per si volem accedir desde python pero per el websocket enviare el json
        self.gas_concentration = 0.0
        self.ultrasound_sensor_1_distance = 0.0
        self.ultrasound_sensor_2_distance = 0.0
        self.dht11_humidity = 0.0
        self.dht11_temp = 0.0
        self.json_value = ""
        # self.ser.reset_input_buffer()
    

    """
    Es subscribe a luci/sensors i reb els valors dels sensors 
    """
    def subscribe(self, client: mqtt_client):
        def on_message(client, userdata, msg):
            print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

        client.subscribe(self.topic)
        client.on_message = on_message

    """
    Es conecta al raspberry per mqtt per rebre els valors dels sensors
    """
    def connect_mqtt(self) -> mqtt_client:
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)

        client = mqtt_client.Client()
        # client.username_pw_set(username, password)
        client.on_connect = on_connect
        client.connect(self.broker, self.port)
        return client

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

    def start_reading(self):
        if self.use_mqtt:
            self.connect_mqtt()

    def read_sensors(self):
        #if self.ser.in_waiting > 0:
        json_text = self.ser.readline().decode('utf-8')
        print(json_text)
        # if json_text is None or len(json_text) < 1:
        #     return self.parse_sensors(self.error_data())
            
        return self.parse_sensors(json_text)
        #else:
        #    print("No data available from arduino yet.")
        #     return self.parse_sensors(self.error_data())
    
    def get_sensor_values(self):
        return self.json_value
    
    def close(self):
        self.ser.close()
    
