import math
class Map:
  def __init__(self, w, h):
    self.map = [[0 for y in range(h)] for x in range(w)]
    self.w = w
    self.h = h
    self.p = type('', (), {})
    self.p.x = int(w/2)
    self.p.y = int(h/2)

  def obstruction(self, thetaDegrees, distance):
    p = self.pos(thetaDegrees, distance)
    self.map[p.x][p.y]=1

  def move(self, thetaDegrees, distance):
    self.p = self.pos(thetaDegrees, distance)    

  def pos(self, thetaDegrees, distance):
    thetaRadians = math.radians(thetaDegrees)
    pos = type('', (), {})
    pos.x = self.p.x + int(distance*math.cos(thetaRadians))
    pos.y = self.p.y + int(distance*math.sin(thetaRadians))
    return pos
   
  def printMap(self):
    for x in range(self.w):
      for y in range(self.h):
        if (self.map[x][y]==1):
          print 'x',
        else:
          print ' ',
      print ''

  
m=Map(100,100)
for i in range(360):
  m.obstruction(i,10)

m.move(45, 50)
for i in range(360):
  m.obstruction(i,10)
m.printMap()

