import math

import random
import sensors
import map
import api
import driver

import time

class Controller:
  def __init__(self):
    self.sensors = sensors.Sensors()
    self.map = map.Map(240,240,10)
    self.api = api.API()
    self.driver = driver.Driver()
    self.turns = 0
    self.direction = True
    self.LANE_WIDTH = 12
    self.FORWARD_DIST = 120
    self.PROXIMITY_DIST = 10
    self.MIN_UNVISITED_AREA = 10
  
 
  def run(self):
    try:
     # self.map.move(self.sensors.measure_compass(),0)
      while(True):       
        # Move to a new location
        print "Moving Turn: ", self.turns
        self.greedy_walk()
        self.map.printMap(80,80)
        self.turns=self.turns+1
    except:
      print "Caught exception, stopping driver"
      self.driver.stop()
      raise

  #
  # The scan algorithm , this method continously scans a room and makes the next move necessary
  #
  '''
  #This algorithim has been commented out and replaced by greedy_walk, as greedy_walk is a different algorithm
  #This algorithm moves in a wavy pattern - it goes up until it hits an obstruction, and moves right creating lanes
  def move(self):
    self.sensors.read()
    if (self.sensors.proximity()):
      # Record the obstruction
      self.map.obstruction(self.sensors.compass(), self.PROXIMITY_DIST)
      # Make a turn
      if (self.direction):
        self.turn_left(90)
        self.forward(self.LANE_WIDTH)
        self.turn_left(90)
        self.direction = False
      else:
        self.turn_right(90)
        self.forward(self.LANE_WIDTH)
        self.turn_right(90)
        self.direction = True
    # Move in a straight line until obstruction discovered
    self.forward(self.FORWARD_DIST)
'''

#This algorithm when it hits an obstruction chooses to turn to the side that has more unvisited area according to the map
  def greedy_walk(self):
      self.sensors.read()
      if (self.sensors.proximity()):
        # Record the obstruction
        self.map.obstruction(self.map.angle, self.PROXIMITY_DIST)
        left_unvisited_area = self.map.unvisited_area(self.wrapAngle(self.map.angle - 90), self.FORWARD_DIST)
        right_unvisited_area = self.map.unvisited_area(self.wrapAngle(self.map.angle + 90), self.FORWARD_DIST)
        # Make a turn
        if max(left_unvisited_area, right_unvisited_area) < self.MIN_UNVISITED_AREA:
            if random.random() > 0.5:
                self.turn_left(90)
            else:
                self.turn_right(90)
        elif left_unvisited_area > right_unvisited_area:
          self.turn_left(90)
        else:
          self.turn_right(90)
      # Move in a straight line until obstruction discovered
      self.forward(self.FORWARD_DIST)




  def forward(self, inches):
    print "Forward: ", inches
    # Read sensors and check for proximity so that if the robot has turned it checks if there is an obstacle in front of it rather than just start moving forward
    self.sensors.read()
    if self.sensors.proximity():
      return
    self.driver.forward(inches)
    progress = 0
    obstructed = False
    # wait while checking for obstructions
    while not self.driver.isDone() and not obstructed:
      new_progress = self.driver.progress()
      diff = new_progress - progress
      rel_dist = diff*inches/100
      if rel_dist > 2:
        self.sensors.read()
        print "Progress = %f new_progress = %f rel_dist = %f compass = %f proximity = %f" % (progress, new_progress, rel_dist, self.sensors.compass(), self.sensors.proximity())
        # Using map angle as dead reckoning should be more accurate, and moving in a straight line
        self.map.move(self.map.angle, rel_dist)
        progress = new_progress
        if self.sensors.proximity():
          self.driver.stop()
          self.map.obstruction(self.map.angle, self.PROXIMITY_DIST)
          obstructed = True
        # Check if the amount of unvisited area in this direction is too little
        unvisited_area = self.map.unvisited_area(self.map.angle, int(progress*inches))
        if unvisited_area < self.MIN_UNVISITED_AREA:
            print "Unvisited Area: %f" % (unvisited_area)
            self.driver.stop()
            break
        # Push the readings to the server
        # TODO: API takes too long to return, so need to cache the map position and sensor values and later push to API when the robot is stopped
        #self.api.push(self.map.p, self.sensors.environment())
      else:
        time.sleep(0.1)
    
  def turn_left(self, deg):
    print "turn_left : ", deg
    self.driver.turn_left(deg)
    self.driver.wait()
    desiredAngle = self.wrapAngle(self.map.angle - deg)
    self.map.move(desiredAngle,0)

  def turn_right(self, deg):
    print "turn_right : ", deg
    self.driver.turn_right(deg)
    self.driver.wait()
    desiredAngle = self.wrapAngle(self.map.angle + deg)
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

 
c = Controller()
c.run()
