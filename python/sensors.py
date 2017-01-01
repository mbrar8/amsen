import sonar
import arduino

class Sensors:
  def __init__(self):
    self.sonar = sonar.Sonar()
    self.arduino = arduino.Arduino()


  def read(self):
    self.sonar.read()
    self.arduino.read()

  def distance(self):
    return self.sonar.distance

  def proximity(self):
    return self.sonar.promximity

  def compass(self):
    return self.arduino.compass()

  def environment(self):
    return self.arduino.environment()

 
