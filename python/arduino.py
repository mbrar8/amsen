import time 
import serial
class Arduino:
	def __init__(self):
		self.data_in = serial.Serial('/dev/ttyACM0', 115200, timeout=2)
                self.data_in.readline()
                self.sensor_input = {}

	def read(self):
		self.sensor_input={}
            	while True:
		  self.data_in.read(self.data_in.inWaiting())
		  var = self.data_in.readline()
		  try:
                    print var
		    parts = var.split(',')
		    print parts
		    for x in parts:
			final = x.split('=')
			self.sensor_input[final[0]] = float(final[1])
                    self.sensor_input['CMP']
		    return
		  except:
		    print "ignoring garbgage"

	def compass(self):
		self.read()
		return self.sensor_input['CMP']

	def environment(self):
		return self.sensor_input;


#a = Arduino()
#while True:
#  print a.compass()
#  time.sleep(1)
