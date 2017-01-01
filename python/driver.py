import servo
import math
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

  def timeToWait(self, inches):
    return inches*self.oneRotationTime/self.circumference

  def turn_left(self, degrees):
    #turn left by degrees
    self.right.clockwise()
    self.left.clockwise()
    inchesToMove = (degrees*8*math.pi)/360
    timeToSleep = self.timeToWait(inchesToMove)
    time.sleep(timeToSleep)
    self.right.stop()
    self.left.stop()

  def turn_right(self, degrees):
    #turn right by degrees
    self.right.anticlockwise()
    self.left.anticlockwise()
    inchesToMove = (degrees*8*math.pi)/360
    timeToSleep = self.timeToWait(inchesToMove)
    time.sleep(timeToSleep)
    self.right.stop()
    self.left.stop()

#d = Driver()
#print "Move 15"
#d.forward(15)
#time.sleep(1)
#print "Turn 90"
#d.turn_left(90)
#time.sleep(1)
#print "Move 8"
#d.forward(8)
#time.sleep(1)
#print "Turn 90"
#d.turn_left(90)
#time.sleep(1)
#print "Move 15"
#d.forward(15)
#time.sleep(1)
#print "Turn 90"
#d.turn_left(90)
#time.sleep(1)
#print "Move 8"
#d.forward(8)
#time.sleep(1)
