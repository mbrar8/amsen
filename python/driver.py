import sys
import time 
from Phidget22.Devices.Stepper import *
from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22.Net import *
import math
import time
from Motor import Motor
class Driver:

  def __init__(self):
    # Instantiate the motors
    self.left = Motor(423918)
    self.right = Motor(423444)
    self.wheel_circumference = math.pi*3.547
    self.robo_circumference = math.pi*10.07
    self.oneRotationTime=20
    self.accl = 800
    self.velocity = 2000


  def wheel_degreesToSteps(self, degrees):
    return degrees*6400/360

  def distanceToSteps(self, inches):
    degrees = inches*360/self.wheel_circumference
    return self.wheel_degreesToSteps(degrees)

  def robo_degreesToSteps(self, degree):
    distance = degree*self.robo_circumference/360
    return self.distanceToSteps(distance)

  def forward(self, inches):
    # move forward by inches
    steps = self.distanceToSteps(inches)
    self.left.turn(-1*steps)
    self.right.turn(steps)
   
  def turn_left(self, degrees):
    #turn left by degrees
    steps = self.robo_degreesToSteps(degrees)
    self.left.turn(-1*steps)
    self.right.turn(-1*steps)
 
  def turn_right(self, degrees):
    #turn left by degrees
    steps = self.robo_degreesToSteps(degrees)
    self.left.turn(steps)
    self.right.turn(steps)

  def stop(self):
    '''
     Stops the motors immediately and returns progress 
    '''
    self.left.stop()
    self.right.stop()
    return self.progress()

  def progress(self):
    return min(self.left.progress, self.right.progress)
 

  def isDone(self):
    return self.left.isDone() and self.right.isDone()
  
  def wait(self):
    print "Waiting for left:%d right:%d" %(self.left.isDone(), self.right.isDone())
    while not self.isDone():
      time.sleep(1)
      print "Waiting for left:%d | %d%% right:%d |%d%%" %(self.left.isDone(), self.left.progress, self.right.isDone(), self.right.progress)

'''
d = Driver()
d.stop()
d.turn_left(1440)
d.wait()
exit()
print "Move 80"
d.forward(80)
d.wait()
print "Move 80 done"
print "Turn Left 360"
d.turn_left(360)
d.wait()
d.forward(80)
d.wait()
print "Turn right 360"
d.turn_right(360)
d.wait()
'''
