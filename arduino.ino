#use arduino ide app
const int moistureSensorPin = A0; // Analog pin connected to the sensor
void setup() {
Serial.begin(9600);
}
void loop() {
int sensorValue = analogRead(moistureSensorPin);
Serial.println(sensorValue); // Send sensor value to serial monitor
delay(1000); // Delay before next reading
}
