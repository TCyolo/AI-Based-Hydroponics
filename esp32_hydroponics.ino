#include "DHT.h"

#define DHTPIN 4
#define DHTTYPE DHT11

#define MOISTURE_PIN 35

#define RELAY_PUMP 26
#define RELAY_LED 25

DHT dht(DHTPIN, DHTTYPE);

void setup() {

Serial.begin(115200);
dht.begin();

pinMode(RELAY_PUMP, OUTPUT);
pinMode(RELAY_LED, OUTPUT);

digitalWrite(RELAY_PUMP, HIGH);
digitalWrite(RELAY_LED, HIGH);

}

void loop() {

float humidity = dht.readHumidity();
float temperature = dht.readTemperature();
int moisture = analogRead(MOISTURE_PIN);

Serial.print(humidity);
Serial.print(",");
Serial.print(temperature);
Serial.print(",");
Serial.println(moisture);

delay(2000);

if (Serial.available()) {

String cmd = Serial.readStringUntil('\n');

if (cmd == "PUMP_ON") digitalWrite(RELAY_PUMP, LOW);
if (cmd == "PUMP_OFF") digitalWrite(RELAY_PUMP, HIGH);

if (cmd == "LED_ON") digitalWrite(RELAY_LED, LOW);
if (cmd == "LED_OFF") digitalWrite(RELAY_LED, HIGH);

}

}
