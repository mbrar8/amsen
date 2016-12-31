import servo
import time
class Driver:

  def __init__(self):
    # Instantiate the servos
    self.left = servo.Servo(8)
    self.right = servo.Servo(10)
    self.oneRotationTime = 0.8
    self.circumference = 10.99
    

  def forward(self, inches):
    # move forward by inches
    self.right.clockwise()
    self.left.anticlockwise()
    time.sleep(inches*self.oneRotationTime/self.circumference)
    self.right.stop()
    self.left.stop()


d = Driver()
d.forward(12)

