import math

import sensors
import map
import api
import driver2

import time

class Controller:
  def __init__(self):
    self.sensors = sensors.Sensors()
    self.map = map.Map(1000,1000)
    self.api = api.API()
    self.driver = driver2.Driver()
    self.turns = 0
    self.direction = True
   
  def run(self):
    self.map.move(self.sensors.measure_compass(),0)
    while(True):
      print "Reading Sensors"
      self.sensors.read()
       
      # Push the readings to the server
      self.api.push(self.map.p, self.sensors.environment())

      # Move to a new location
      print "Moving Turn: ", self.turns
      self.move()
      self.turns=self.turns+1

  #
  # The scan algorithm , this method continously scans a room and makes the next move necessary
  #
  def move(self):
    self.sensors.read()
    if (self.sensors.proximity()):
      # Record the obstruction
      self.map.obstruction(self.sensors.compass(), 1)
      # Make a turn
      if (self.direction):
        self.turn_left(90)
        self.forward(24)
        self.turn_left(90)
        self.direction = False
      else:
        self.turn_right(90)
        self.forward(24)
        self.turn_right(90)
        self.direction = True
    self.forward(12)
 
  def forward(self, inches):
    print "Forward: ", inches
    self.driver.forward(inches)
    # wait while checking for obstructions
    distance_moved = inches
    while not self.driver.isDone():
      self.sensors.read()
      print "moving forward , checking proximity: ", self.sensors.proximity()
      if self.sensors.proximity():
	progress = self.driver.stop()
        distance_moved *= progress/100
        self.map.obstruction(self.sensors.compass(), distance_moved + 1)
        break
      time.sleep(0.1)

    self.map.move(self.sensors.measure_compass(), distance_moved)
    
  def turn_left(self, deg):
    print "turn_left : ", deg
    self.driver.turn_left(deg)
    self.driver.wait()
    desiredAngle = self.wrapAngle(self.map.angle - deg)
    #self.align(desiredAngle)
    self.map.move(desiredAngle,0)

  def turn_right(self, deg):
    print "turn_right : ", deg
    self.driver.turn_right(deg)
    self.driver.wait()
    desiredAngle = self.wrapAngle(self.map.angle + deg)
    #self.align(desiredAngle)
    self.map.move(desiredAngle,0)

  # 
  # Ensures the angle stays between [0 - 360)
  #
  def wrapAngle(self, angle):
    desiredAngle =angle
    # handle the negative case
    if (desiredAngle < 0):
      desiredAngle = desiredAngle + 360
    if (desiredAngle >= 360):
      desiredAngle = desiredAngle % 360
    return desiredAngle

  def align(self, act):
    
    print "ALIGN: " 
    pos = self.sensors.measure_compass()
    diff = abs(pos - act)
	
    while diff >= 4:
        print "POS: " , pos, "\tACT: ", act, "\tDIFF:",diff
	if pos < act:
	   self.driver.turn_right(1)
	   print "Adjusting: Turning right by 4" 
	else:
	   self.driver.turn_left(1)
	   print "Adjusting: Turning left by 4"
        self.driver.wait()
	pos = self.sensors.measure_compass()
        diff = abs(pos - act)
        time.sleep(0.5)
   
    print "POS: " , pos, "\tACT: ", act, "\tDIFF:",diff
c = Controller()
c.run()
