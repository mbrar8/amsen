import math

class MapException(Exception):
  pass

class Map:
    def __init__(self, w, h, scale):
        self.SCALE = scale
        self.w = w * self.SCALE
        self.h = h * self.SCALE
        self.map = [[0 for x in range(self.w)] for y in range(self.h)]
        self.p = type('', (), {})
        self.p.x = int(self.w / 2)
        self.p.y = int(self.h / 2)
        self.SONAR_RANGE = 10

        # bounding box for the visited or obstructed area
        # makes it easier to visualize
        self.BOUNDING_MARGIN = self.SCALE * 4
        self.b_s_x = self.p.x - self.BOUNDING_MARGIN
        self.b_s_y = self.p.y - self.BOUNDING_MARGIN
        self.b_e_x = self.p.x + self.BOUNDING_MARGIN
        self.b_e_y = self.p.y + self.BOUNDING_MARGIN

        self.angle = 0

    def obstruction(self, thetaDegrees, distance):
        angle = thetaDegrees - self.SONAR_RANGE
        while (angle <= thetaDegrees + self.SONAR_RANGE):
            p = self.pos(angle, distance)
            if p.y >= 0 and p.y < self.h and p.x >= 0 and p.x < self.w:
                self.map[p.y][p.x] = 1
            else:
                raise MapException("Invalid Position: p.y: %d, p.x: %d, po.y: %d, po.x: %d, angle: %f, distance: %d" % (
                p.y, p.x, self.p.y, self.p.x, angle, distance))
            angle += 0.1
        return p

    def move(self, thetaDegrees, distance):
        self.p = self.pos(thetaDegrees, distance)
        self.angle = thetaDegrees
        if self.p.y >= 0 and self.p.y < self.h and self.p.x >= 0 and self.p.x < self.w:
            self.map[self.p.y][self.p.x] = 2
        else:
            raise MapException("Invalid Position: p.y: %d, p.x: %d" % (self.p.y, self.p.x))

    def pos(self, thetaDegrees, distance):
        scaled_distance = distance * self.SCALE
        thetaRadians = math.radians(thetaDegrees)
        pos = type('', (), {})
        pos.x = self.p.x + int(scaled_distance * math.cos(thetaRadians))
        pos.y = self.p.y + int(scaled_distance * math.sin(thetaRadians))

        # recompute the bounding box
        self.b_s_x = max(0, min(self.b_s_x, pos.x - self.BOUNDING_MARGIN))
        self.b_e_x = min(self.w, max(self.b_e_x, pos.x + self.BOUNDING_MARGIN))
        self.b_s_y = max(0, min(self.b_s_y, pos.y - self.BOUNDING_MARGIN))
        self.b_e_y = min(self.h, max(self.b_e_y, pos.y + self.BOUNDING_MARGIN))
        return pos

    #
    # Checks if there is any obstruction along the current direction upto given distance
    #
    def isBlocked(self, distance):
        for d in range(distance):
            p = self.pos(self.angle, d)
            if (self.map[p.y][p.x] == 1):
                return True
        return False

    def printMap(self, screen_width, screen_height):
        # Lets make sure screen area is less than equal to the actual map
        bw = (self.b_e_x - self.b_s_x)
        bh = (self.b_e_y - self.b_s_y)
        sw = min(screen_width, bw)
        sh = min(screen_height, bh)
        # Map width to screen width ratio
        m_s_w = bw / sw
        # Map height to screen height ratio
        m_s_h = bh / sh



        # Iterate over the screen width and height
        for sx in range(sw):
            for sy in range(sh):
                v = 0
                # For every screen pixel we will end up mapping a rectangle of m_s_w X m_s_h
                # we have to approximate the value of that entire rectangle to a single pixel
                for ix in range(m_s_w):
                    for iy in range(m_s_h):
                        x = self.b_s_x + sx * m_s_w + ix
                        y = self.b_s_y + sy * m_s_h + iy
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

'''

m = Map(100, 100, 10)
for i in range(40):
    m.move(0, 0.3)
for i in range(50):
    m.move(90, 0.3)
for i in range(50):
    m.move(180, 0.3)
for i in range(50):
    m.move(270, 0.3)
for i in range(100):
    m.move(-45, 0.3)
for i in range(100):
    m.move(-135, 0.3)
for i in range(40):
    m.move(0, 0.3)
for i in range(50):
    m.move(90, 0.3)
for i in range(50):
    m.move(180, 0.3)
for i in range(50):
    m.move(270, 0.3)

m.printMap(30, 60)
'''