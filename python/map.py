import math

class MapException(Exception):
  pass

class Map:
  def __init__(self, w, h, scale):
    self.SCALE = scale
    self.w = w*self.SCALE
    self.h = h*self.SCALE
    self.map = [[0 for x in range(self.w)] for y in range(self.h)]
    self.p = type('', (), {})
    self.p.x = int(self.w/2)
    self.p.y = int(self.h/2)
    self.angle = 0

  def obstruction(self, thetaDegrees, distance):
    angle = thetaDegrees-2
    while(angle <=thetaDegrees+2):
      p = self.pos(angle, distance)
      if p.y >= 0 and p.y < self.h and p.x >= 0 and p.x < self.w:
       self.map[p.y][p.x] = 1
      else:
       raise MapException("Invalid Position: p.y: %d, p.x: %d, po.y: %d, po.x: %d, angle: %f, distance: %d" % (p.y, p.x, self.p.y, self.p.x, angle, distance))
      angle+=0.1
    return p

  def move(self, thetaDegrees, distance):
    self.p = self.pos(thetaDegrees, distance)
    self.angle = thetaDegrees
    if self.p.y >= 0 and self.p.y < self.h and self.p.x >= 0 and self.p.x < self.w:
      self.map[self.p.y][self.p.x] = 2
    else:
     raise MapException("Invalid Position: p.y: %d, p.x: %d" % (self.p.y, self.p.x))


  def pos(self, thetaDegrees, distance):
    scaled_distance = distance*self.SCALE
    thetaRadians = math.radians(thetaDegrees)
    pos = type('', (), {})
    pos.x = self.p.x + int(scaled_distance*math.cos(thetaRadians))
    pos.y = self.p.y + int(scaled_distance*math.sin(thetaRadians))
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
   
  def printMap(self, screen_width, screen_height):
    # Lets make sure screen area is less than equal to the actual map
    sw = min(screen_width, self.w)
    sh = min(screen_height, self.h)

    # Map width to screen width ratio
    m_s_w = self.w/sw
    # Map height to screen height ratio
    m_s_h = self.h/sh

    # Iterate over the screen width and height
    for sx in range(sw):
      for sy in range(sh):
         v = 0
         # For every screen pixel we will end up mapping a rectangle of m_s_w X m_s_h
         # we have to approximate the value of that entire rectangle to a single pixel
         for ix in range(m_s_w):
           for iy in range(m_s_h):
             x = min(sx * m_s_w + ix, self.w-1)
             y = min(sy * m_s_h + iy, self.h-1)
             if self.map[y][x] == 1:
               v = 1
               break
             elif self.map[y][x] == 2:
               v = 2
           if v == 1:
	     break

         if v == 1:
           print 'x',
         elif v == 2:
           print '.',
         else:
           print ' ',
      print '|'
    for sx in range(sw):
      print '_'  
