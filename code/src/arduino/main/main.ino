// DHT Temperature & Humidity Sensor
// Unified Sensor Library Example
// Written by Tony DiCola for Adafruit Industries
// Released under an MIT license.

// REQUIRES the following Arduino libraries:
// - DHT Sensor Library: https://github.com/adafruit/DHT-sensor-library
// - Adafruit Unified Sensor Lib: https://github.com/adafruit/Adafruit_Sensor

#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <DHT_U.h>
#include "ArduinoJson.h"

// TODOS LOS PINS A DEFINIR

// MOTOR B
#define EnB 6
#define inB1 5
#define inB2 8

// MOTOR A
#define EnA 9
#define inA1 10
#define inA2 13

// MOTOR VARIABLES
String inString = "";    // concatenació de tota la instrucció
int inChar = 0;          // valor rebut actualment
int thruster_left;       // valor motor esquerra
int thruster_right;      // valor motor dret
int save_as_second = false; // flag per saber a quin motor guardar el valor

// ULTRASOUND SENSOR 1
#define UltraSoundTrigPin_1 7
#define UltraSoundEchoPin_1 3

// ULTRASOUND SENSOR 2
#define UltraSoundTrigPin_2 12
#define UltraSoundEchoPin_2 11

#define DHTPIN 2     // Digital pin connected to the DHT sensor 

const int MQ_PIN = A0;      // Pin del sensor


// DHT 1 SENSOR VARIABLES (TEMPERATURE & HUMIDITY)
#define DHTTYPE    DHT11     // Utilitzem el DHT 11
DHT_Unified dht(DHTPIN, DHTTYPE);

uint32_t delayMS;

// GAS SENSOR VARIABLES

const int RL_VALUE = 5;      // Resistencia RL del modulo en Kilo ohms
const int R0 = 10;          // Resistencia R0 del sensor en Kilo ohms
// Datos para lectura multiple
const int READ_SAMPLE_INTERVAL = 100;    // Tiempo entre muestras
const int READ_SAMPLE_TIMES = 5;       // Numero muestras
// Ajustar estos valores para vuestro sensor según el Datasheet
// (opcionalmente, según la calibración que hayáis realizado)
const float X0 = 200;
const float Y0 = 1.7;
const float X1 = 10000;
const float Y1 = 0.28;
// Puntos de la curva de concentración {X, Y}
const float punto0[] = { log10(X0), log10(Y0) };
const float punto1[] = { log10(X1), log10(Y1) };
// Calcular pendiente y coordenada abscisas
const float scope = (punto1[1] - punto0[1]) / (punto1[0] - punto0[0]);
const float coord = punto0[1] - punto0[0] * scope;


void initL298nPins(){
   pinMode (inA1, OUTPUT);
   pinMode (inA2, OUTPUT);
   pinMode (inB1, OUTPUT);
   pinMode (inB2, OUTPUT);
   pinMode (EnA, OUTPUT);
   pinMode (EnB, OUTPUT);
}

void initDHTSensor() {
  // Initialize device.
  dht.begin();
  Serial.println(F("DHTxx Unified Sensor Example"));
  // Print temperature sensor details.
  sensor_t sensor;
  dht.temperature().getSensor(&sensor);
  Serial.println(F("------------------------------------"));
  Serial.println(F("Temperature Sensor"));
  Serial.print  (F("Sensor Type: ")); Serial.println(sensor.name);
  Serial.print  (F("Driver Ver:  ")); Serial.println(sensor.version);
  Serial.print  (F("Unique ID:   ")); Serial.println(sensor.sensor_id);
  Serial.print  (F("Max Value:   ")); Serial.print(sensor.max_value); Serial.println(F("°C"));
  Serial.print  (F("Min Value:   ")); Serial.print(sensor.min_value); Serial.println(F("°C"));
  Serial.print  (F("Resolution:  ")); Serial.print(sensor.resolution); Serial.println(F("°C"));
  Serial.println(F("------------------------------------"));
  // Print humidity sensor details.
  dht.humidity().getSensor(&sensor);
  Serial.println(F("Humidity Sensor"));
  Serial.print  (F("Sensor Type: ")); Serial.println(sensor.name);
  Serial.print  (F("Driver Ver:  ")); Serial.println(sensor.version);
  Serial.print  (F("Unique ID:   ")); Serial.println(sensor.sensor_id);
  Serial.print  (F("Max Value:   ")); Serial.print(sensor.max_value); Serial.println(F("%"));
  Serial.print  (F("Min Value:   ")); Serial.print(sensor.min_value); Serial.println(F("%"));
  Serial.print  (F("Resolution:  ")); Serial.print(sensor.resolution); Serial.println(F("%"));
  Serial.println(F("------------------------------------"));
  // Set delay between sensor readings based on sensor details.
  delayMS = sensor.min_delay / 1000;
  Serial.println(delayMS);

}

void setup() {
  Serial.begin(9600);
  initDHTSensor();
  initL298nPins();
}

float readDHTTemp() {
  // Get temperature event and print its value.
  sensors_event_t event;
  dht.temperature().getEvent(&event);
  if (isnan(event.temperature)) {
    Serial.println(F("Error reading temperature!"));

    return 0.0;
  }
  else {
    return event.temperature;
  }
}

float readDHTHumidity() {
  // Get humidity event and print its value.
  sensors_event_t event;
  dht.humidity().getEvent(&event);
  if (isnan(event.relative_humidity)) {
    Serial.println(F("Error reading humidity!"));

    return 0.0;
  }
  else {
    return event.relative_humidity;
  }
}

// Obtener la resistencia promedio en N muestras
float readMQ(int mq_pin)
{
  float rs = 0;
  for (int i = 0; i < READ_SAMPLE_TIMES; i++) {
    rs += getMQResistance(analogRead(mq_pin));
    delay(READ_SAMPLE_INTERVAL);
  }
  return rs / READ_SAMPLE_TIMES;
}
// Obtener resistencia a partir de la lectura analogica
float getMQResistance(int raw_adc)
{
  return (((float)RL_VALUE / 1000.0 * (1023 - raw_adc) / raw_adc));
}
// Obtener concentracion 10^(coord + scope * log (rs/r0)
float getConcentration(float rs_ro_ratio)
{
  return pow(10, coord + scope * log(rs_ro_ratio));
}




long readUltrasonicDistance (int triggerPin, int echoPin)
{
  pinMode (triggerPin, OUTPUT); // Clear the trigger
  digitalWrite (triggerPin, LOW) ;
  delayMicroseconds (2);
  // Sets the trigger pin to HIGH state for 10 microseconda
  digitalWrite (triggerPin, HIGH);
  delayMicroseconds (10);
  digitalWrite (triggerPin, LOW) ;
  pinMode (echoPin, INPUT);
  // Reads the echo pin, and returns the sound wave travel time
  return pulseIn (echoPin, HIGH);
}

// Funcions pels motors
void motors_forward( int speed)
{
  if (speed < 0) speed =0;
  if (speed > 255) speed = 255;
  
 //dirreccio motor A
 digitalWrite (inA1, HIGH);
 digitalWrite (inA2, LOW);
 analogWrite (EnA, speed); 
 //direccio motor B
 digitalWrite (inB1, HIGH);
 digitalWrite (inB2, LOW);
 analogWrite (EnB, speed); 
}

void motors_backward ( int speed)
{
  if (speed < 0) speed =0;
  if (speed > 255) speed = 255;
  
 //dirreccio motor A
 digitalWrite (inA1, LOW);
 digitalWrite (inA2, HIGH);
 analogWrite (EnA, speed); 
 //direccio motor B
 digitalWrite (inB1, LOW);
 digitalWrite (inB2, HIGH);
 analogWrite (EnB, speed);
}

void motors_turn_forward( int speed_left, int speed_right)
{
  if (speed_left < 0) speed_left =0;
  if (speed_left > 255) speed_left = 255;
  if (speed_right < 0) speed_right =0;
  if (speed_right > 255) speed_right = 255;
    
 digitalWrite (inA1, HIGH);
 digitalWrite (inA2, LOW);
 analogWrite (EnA, speed_left); 

 digitalWrite (inB1, HIGH);
 digitalWrite (inB2, LOW);
 analogWrite (EnB, speed_right);
}

void motors_turn_left_still( int speed)
{
  if (speed < 0) speed =0;
  if (speed > 255) speed = 255;
  
 digitalWrite (inA1, LOW);
 digitalWrite (inA2, HIGH);
 analogWrite (EnA, speed); 
 
 digitalWrite (inB1, HIGH);
 digitalWrite (inB2, LOW);
 analogWrite (EnB, speed); 
}

void motors_turn_right_still( int speed)
{
  if (speed < 0) speed =0;
  if (speed > 255) speed = 255;
  
 digitalWrite (inA1, HIGH);
 digitalWrite (inA2, LOW);
 analogWrite (EnA, speed); 
 digitalWrite (inB1, LOW);
 digitalWrite (inB2, HIGH);
 analogWrite (EnB, speed); 
}

void motors_stop()
{
 digitalWrite (inA1, LOW);
 digitalWrite (inA2, LOW);
 analogWrite (EnA, 0); 
 digitalWrite (inB1, LOW);
 digitalWrite (inB2, LOW);
 analogWrite (EnB, 0);
}

void motors_read_serial() {
  // El serial read funciona amb el format "10,0;" (sense les cometes).
  // L'exemple significa que el motor esquerra va a velocitat 10 i el dret a velocitat 0.
  
  /// Read serial data
  if (Serial.available()) {  // si serial data està disponible
    inChar = Serial.read();  // guardem l'últim byte
    inString += char(inChar);// concatenem
        
    /// quan detectem una coma, guardem el valor i l'assignem a left
    if (inChar == ',') {
      if (save_as_second == false) { 
        thruster_left = inString.toInt(); 
        inString = "";               
        save_as_second == true;      
      }
    }
    /// al detectar una semicolon, guardem l'últim valor a Right
    if (inChar == ';') {     
      thruster_right = inString.toInt();
      inString = "";        
      save_as_second = false;

      /// Ja tenim tots els valors necessaris, movem el motor
      Serial.print("Left Thruster:"); 
      Serial.println(thruster_left);
      Serial.print("Right string: ");
      Serial.println(thruster_right);

      //TODO: millorar el moviment dels motors. Veure els símbols de cada valors per saber quina funció cridar.
      motors_turn_forward(thruster_left, thruster_right);
      
    }
  }
}

DynamicJsonDocument doc(1024);

void loop() {
  motors_read_serial();
  // Delay between measurements.
  /*
  delay(delayMS);

  float dht11_temp = readDHTTemp();
  float dht11_humidity = readDHTHumidity();

  int ultrasound_sensor_1_distance = 0.01723 * readUltrasonicDistance (UltraSoundTrigPin_1, UltraSoundEchoPin_1);
  int ultrasound_sensor_2_distance = 0.01723 * readUltrasonicDistance (UltraSoundTrigPin_2, UltraSoundEchoPin_2);

  float rs_med = readMQ(MQ_PIN);      // Obtener la Rs promedio
  float gas_concentration = getConcentration(rs_med / R0); // Obtener la concentración

  doc["gas_concentration"] = gas_concentration;
  doc["ultrasound_sensor_1_distance"]   = ultrasound_sensor_1_distance;
  doc["ultrasound_sensor_2_distance"]   = ultrasound_sensor_2_distance;
  doc["dht11_humidity"] = dht11_humidity;
  doc["dht11_temp"] = dht11_temp;

  serializeJson(doc, Serial);
  Serial.println("");
  */
}
