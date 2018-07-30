import time

import arduino
import driver


device1 = '/dev/ttyACM0'
device2 = '/dev/ttyACM1'
a1 = arduino.Arduino(device1)
a2 = arduino.Arduino(device2)
d = driver.Driver
while True:
    d.stop()
    print("Move forward 5")
    d.forward(5)
    d.wait()
    print("Reading")
    a1.read()
    a2.read()
    print(device1 + str(a1.sensor_input))
    print(device2 + str(a2.sensor_input))
    print("Turn left 90 degrees")
    d.turn_left(90)
    d.wait()
    time.sleep(1)
