import math
class Map:
  def __init__(self, w, h):
    self.map = [[0 for x in range(w)] for y in range(h)]
    self.w = w
    self.h = h
    self.p = type('', (), {})
    self.p.x = int(w/2)
    self.p.y = int(h/2)
    self.angle = 0

  def obstruction(self, thetaDegrees, distance):
    angle = thetaDegrees-2
    while(angle <=thetaDegrees+2):
      p = self.pos(angle, distance)
      self.map[p.y][p.x]=1
      angle+=0.1
    return p

  def move(self, thetaDegrees, distance):
    self.p = self.pos(thetaDegrees, distance)
    self.angle = thetaDegrees   

  def pos(self, thetaDegrees, distance):
    thetaRadians = math.radians(thetaDegrees)
    pos = type('', (), {})
    pos.x = self.p.x + int(distance*math.cos(thetaRadians))
    pos.y = self.p.y + int(distance*math.sin(thetaRadians))
    return pos
  
  #
  # Checks if there is any obstruction along the current direction upto given distance
  #
  def isBlocked(self, distance):
    for d in range(distance):
      p = self.pos(self.angle, d)
      if (self.map[p.y][p.x]==1):
        return True
    return False
   
  def printMap(self):
    for x in range(self.w):
      for y in range(self.h):
        if (self.map[y][x]==1):
          print 'x',
        else:
          print ' ',
      print ''

  
#m=Map(200,100)
#for i in range(360):
#  m.obstruction(i,10)
#
#m.move(90, 10)
#for i in range(360):
#  m.obstruction(i,10)
#m.printMap()

