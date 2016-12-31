import serial
class Arduino:
	def __init__(self):
		self.data_in = serial.Serial('/dev/ttyACM0', 115200, timeout=2)
                self.data_in.readline()
                self.sensor_input = {}

	def read(self):
		self.sensor_input={}
		var = self.data_in.readline()
		parts = var.split(',')
		for x in parts:
			final = x.split('=')
			self.sensor_input[final[0]] = float(final[1])
