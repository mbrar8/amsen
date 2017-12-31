import sonar
import arduino

class Sensors:
  def __init__(self):
    self.arduino = arduino.Arduino()

  def read(self):
    self.arduino.read()

  def proximity(self):
    dist = self.arduino.sonar();
    return dist > 0 and dist < 10 

  def compass(self):
    return self.arduino.compass()

  def measure_compass(self):
    return self.arduino.measure_compass()

  def environment(self):
    return self.arduino.environment()

 
