import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import serial
import time


data = pd.read_csv("hydroponics_ai_dataset.csv")

X = data[['humidity','temperature','moisture']]
pump = data['pump']
led = data['led']

pump_model = DecisionTreeClassifier()
led_model = DecisionTreeClassifier()

pump_model.fit(X, pump)
led_model.fit(X, led)

print("model trained")


ser = serial.Serial('COM3', 115200, timeout=1)
time.sleep(5)  
ser.reset_input_buffer()

print("Connected to ESP32")


try:
    while True:

        raw_bytes = ser.readline()
        print("RAW BYTES:", raw_bytes)  

        line = raw_bytes.decode(errors="ignore").strip()

        
        if not line or "," not in line:
            continue

        print("CLEAN:", line)

        try:
            humidity, temperature, moisture = map(float, line.split(","))
        except:
            print("Parse error")
            continue

       
        input_data = pd.DataFrame(
            [[humidity, temperature, moisture]],
            columns=['humidity','temperature','moisture']
        )

        pump_result = pump_model.predict(input_data)[0]
        led_result = led_model.predict(input_data)[0]


        if moisture < 3500:
            pump_result = 0  

        
        if pump_result == 1:
            ser.write(b'PUMP_ON\n')
            print("Pump ON")
        else:
            ser.write(b'PUMP_OFF\n')
            print("Pump OFF")

        if led_result == 1:
            ser.write(b'LED_ON\n')
            print("LED ON")
        else:
            ser.write(b'LED_OFF\n')
            print("LED OFF")

except KeyboardInterrupt:
    print("\nStopped cleanly")
    ser.close()
