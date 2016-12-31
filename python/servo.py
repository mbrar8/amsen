import RPi.GPIO as GPIO

class Servo:
	def __init__(self, pin):
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(pin, GPIO.OUT)
		self.pwm = GPIO.PWM(pin, 100)
	
	def clockwise(self):
		self.pwm.start(1.0)

	def anticlockwise(self):
		self.pwm.start(20)

        def stop(self):
             	self.pwm.stop()

