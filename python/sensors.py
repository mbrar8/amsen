import arduino

class Sensors:
  def __init__(self):
    self.arduino = arduino.Arduino()

  def read(self):
    self.arduino.read()

  def proximity(self):
    sonarArray = self.arduino.sonar()
    sonarProxArray = sonarArray
    anyProx = False
    #Have to look at each individual case as each sonar has a different arrangement
    if 0 < sonarArray[0] < 10:
      sonarProxArray[0] = True
      anyProx = True
    else:
      sonarProxArray[0] = False
    if 0 < sonarArray[1] < 10:
      sonarProxArray[1] = True
      anyProx = True
    else:
      sonarProxArray[1] = False
    if 0 < sonarArray[2] < 10:
      sonarProxArray[2] = True
      anyProx = True
    else:
      sonarProxArray[2] = False
    if 0 < sonarArray[3] < 10:
      sonarProxArray[3] = True
      anyProx = True
    else:
      sonarProxArray[3] = False
    if 0 < sonarArray[4] < 10:
      sonarProxArray[4] = True
      anyProx = True
    else:
      sonarProxArray[4] = False
    if 0 < sonarArray[5] < 10:
      sonarProxArray[5] = True
      anyProx = True
    else:
      sonarProxArray[5] = False
    if 0 < sonarArray[6] < 10:
      sonarProxArray[6] = True
      anyProx = True
    else:
      sonarProxArray[6] = False
    sonarProxArray.append(anyProx)
    return sonarProxArray

  def compass(self):
    return self.arduino.compass()

  def measure_compass(self):
    return self.arduino.measure_compass()

  def environment(self):
    return self.arduino.environment()

 
