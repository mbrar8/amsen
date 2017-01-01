import RPi.GPIO as GPIO
import time

class Servo:
	def __init__(self, pin):
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(pin, GPIO.OUT)
		self.pwm = GPIO.PWM(pin, 100)
           	self.pin = pin

	def reset(self):
		GPIO.setup(self.pin, GPIO.OUT)
		self.pwm = GPIO.PWM(self.pin, 100)
			
	def clockwise(self):
		self.reset()
                self.pwm.start(1.0)

	def anticlockwise(self):
		self.reset()
                self.pwm.start(30.0)

        def stop(self):
             	self.pwm.stop()


