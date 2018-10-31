import time

import arduino

arduino_sonar = arduino.Arduino('/dev/ttyACM0')
while True:
    arduino_sonar.read()
    print(arduino_sonar.sensor_input)
    time.sleep(1)