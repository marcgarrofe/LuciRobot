import serial
import json 
class sensors:
    def __init__(self, port='/dev/ttyACM0', baudrate=9600):
        self.ser = serial.Serial(port, baudrate)

        # ho tenim com objecte per si volem accedir desde python pero per el websocket enviare el json
        self.gas_concentration = 0.0
        self.ultrasound_sensor_1_distance = 0.0
        self.dht11_humidity = 0.0
        self.dht11_temp = 0.0

    
    def parse_sensors(self, json_text):
        json_dict = json.loads(json_text)

        self.gas_concentration = json_dict['gas_concentration']
        self.ultrasound_sensor_1_distance = json_dict['ultrasound_sensor_1_distance']
        self.dht11_humidity = json_dict['dht11_humidity']
        self.dht11_temp = json_dict['dht11_temp']
        
        return json_text

    def read_sensors(self):
        json_text = self.ser.readline()

        if json_text is None:
            raise Exception("Sensor Error")
        
        return self.parse_sensors(json_text)
        
    
    def close(self):
        self.ser.close()
    
