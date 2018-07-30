import time 
import serial


class Arduino:
    def __init__(self, device):
        self.device = device
        self.data_in = serial.Serial(self.device, 115200, timeout=2)
        self.data_in.readline()
        self.sensor_input = {}

    def read(self):
        self.sensor_input={}
        self.data_in.read(self.data_in.inWaiting())
        var = self.data_in.readline()
        try:
            parts = var.split(',')
            print parts
            for x in parts:
                final = x.split('=')
                self.sensor_input[final[0]] = float(final[1])
            # Check that compass and sonar value present in sensor_input, if missing than it's garbage value to ignore
            self.sensor_input['CMP']
            self.sensor_input['SNR']
            return
        except:
            print "ignoring garbage"

    def measure_compass(self):
        self.read()
        return self.sensor_input['CMP']

    def measure_sonar(self):
        self.read()
        return self.sensor_input['SNR']

    def compass(self):
        return self.sensor_input['CMP']
        
    def sonar(self):
        return self.sensor_input['SNR']

    def environment(self):
        return self.sensor_input




