import serial

class Sonar:
  
  def __init__(self):
    # Initialze the variables
    self.prox = False
    self.dist = 100
    self.fail = False
    try: 
      self.ser = serial.Serial("/dev/ttyUSB0", 57600)
    except:
      self.ser = serial.Serial("/dev/ttyUSB1", 57600)
  
  # Read the serial port and align until we have a valid value  
  def align(self):
    while(True):
      ch = self.ser.read()
      if (ch == 'P'):
        return

  
  def read(self):
    # Clear all the existing buffer first, we only want latest values
    self.ser.read(self.ser.inWaiting())
    self.align()
    
    self.prox = self.ser.read() == '1'
    self.ser.read() # 0x0d
    if (self.ser.read()!='R'):
      self.fail = True
      return

    b2 = self.ser.read()
    b1 = self.ser.read()
    b0 = self.ser.read()
    
    self.dist = int('{0}{1}{2}'.format(b2,b1,b0))
    print "SONAR: ",self.dist, " PROXIMITY: " , self.prox
    self.fail = False

  def proximity(self):
    self.read()
    return self.prox

  def distance(self):
    self.read()
    return self.dist

   
