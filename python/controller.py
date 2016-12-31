import sensors
import map
import api
import driver

import time

class Controller:
  def __init__(self):
    self.sensors = Sensors()
    self.map = Map(100,100)
    self.api = Api()
    self.driver = Driver()
    self.api_update = int(time.time())
   
  def run(self):
    while(True):
      self.sensors.read()
      if (self.sensors.distance < 30):
        self.map.obstruction(self.sensors.compass(), self.sensors.distance)
      
      # Every 30 second send the map 
      now = int(time.time())
      if (now - self.api_update > 30):
        self.api.push(self.map)
      
      # Move to a new location
      self.move()

  def move(self):
    self.driver.forward(10):
    self.map.move(self.sensors.compass(),10)  
