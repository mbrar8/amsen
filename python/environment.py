import time
class Environment:
  def __init__(self):
    self.data={} 

  def update(self, reading, position):
    now = time.time
    self.data[now,position.y,position.x] = reading

  
  
