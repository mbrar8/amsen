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
        self.SONAR_RANGE = 5
        self.ROBOT_OBSTRUCTION_DIAMETER = 11 * self.SCALE

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
            self._mark(p.x, p.y, 1)
            angle += 0.1
        return p

    def move(self, thetaDegrees, distance):
        '''
        Move the current position on the map distance inches along thetaDegree straight line
        This method assumes the robot took a straight line path from original position to the new position
        Fills in all the points along the width
        :param thetaDegrees:
        :param distance:
        :return:
        '''
        original_p = self.p
        self.p = self.pos(thetaDegrees, distance)
        self.angle = thetaDegrees

        # Mark all points between original_p and self.p as visited
        delta_x = abs(self.p.x - original_p.x)
        delta_y = abs(self.p.y - original_p.y)
        if delta_x > 0:
            dir_x = (self.p.x - original_p.x) / delta_x
        else:
            dir_x = 0
        if delta_y > 0:
            dir_y = (self.p.y - original_p.y) / delta_y
        else:
            dir_y = 0

        # we will iterate over the x or y which ever has higher delta
        thetaRadians = math.radians(thetaDegrees)
        if delta_x > delta_y:
            for dx in range(delta_x):
                x = min(self.w, max(0, original_p.x + dir_x * dx))
                dy = int(dx * math.tan(thetaRadians))
                y = min(self.h, max(0, original_p.y + dir_y * dy))
                # mark the entire width of the robot
                for wy in range(y - self.ROBOT_OBSTRUCTION_DIAMETER / 2, y + self.ROBOT_OBSTRUCTION_DIAMETER / 2):
                    self._mark(x, wy, 2)
        else:
            for dy in range(delta_y):
                y = min(self.h, max(0, original_p.y + dir_y * dy))
                dx = int(dy * math.tan(thetaRadians))
                x = min(self.w, max(0, original_p.x + dir_x * dx))
                for wx in range(x - self.ROBOT_OBSTRUCTION_DIAMETER / 2, x + self.ROBOT_OBSTRUCTION_DIAMETER / 2):
                    self._mark(wx, y, 2)

    def _mark(self, x, y, value):
        '''
        Private method for marking a single point on the map
        :param x: x -coordinate on the map
        :param y: y -coordinate on the map
        :param value: value for the point. Valid values are 1 for obstruction, 2 for visited
        '''
        # we need to mark all points along the straight line original_p to p as visited
        if self._in_range(x, y):
            self.map[y][x] = value
            # recompute the bounding box
            self.b_s_x = max(0, min(self.b_s_x, x - self.BOUNDING_MARGIN))
            self.b_e_x = min(self.w, max(self.b_e_x, x + self.BOUNDING_MARGIN))
            self.b_s_y = max(0, min(self.b_s_y, y - self.BOUNDING_MARGIN))
            self.b_e_y = min(self.h, max(self.b_e_y, y + self.BOUNDING_MARGIN))
        else:
            raise MapException("Invalid Position: y: %d, x: %d" % (y, x))

    def pos(self, thetaDegrees, distance):
        scaled_distance = distance * self.SCALE
        thetaRadians = math.radians(thetaDegrees)
        pos = type('', (), {})
        pos.x = self.p.x + int(scaled_distance * math.cos(thetaRadians))
        pos.y = self.p.y + int(scaled_distance * math.sin(thetaRadians))
        return pos

    def _in_range(self, x, y):
        '''
        Check if the given point is within the map range
        :param x:
        :param y:
        :return:
        '''
        return y >= 0 and y < self.h and x >= 0 and x < self.w

    def isBlocked(self, distance):
        '''
        Checks if there is any obstruction along the current direction upto given distance
        :param distance:
        :return:
        '''
        for d in range(distance):
            p = self.pos(self.angle, d)
            if not self._in_range(p.x, p.y):
                return True
            if (self.map[p.y][p.x] == 1):
                return True
        return False

    def unvisited_area(self, angle, distance):
        '''
        Returns the area in the direction of angle that is not visited yet
        :param angle: direction the robot will be pointing
        :param distance: total distance the robot will be moving
        :return: number of unvisited points the robot will encounter
        '''
        unvisited = 0
        for d in range(distance):
            p = self.pos(angle, d)
            if not self._in_range(p.x, p.y):
                break
            if self.map[p.y][p.x] == 0:
                unvisited = unvisited + 1
            if self.map[p.y][p.x] == 1:
                break
        return unvisited

    def is_un_visited(self, p):
        return self.map[p.y][p.x] == 0

    def printMap(self, screen_width, screen_height):
        # Lets make sure screen area is less than equal to the actual map
        self.b_e_x = self.w
        self.b_e_y = self.h
        self.b_s_x = 0
        self.b_s_y = 0
        bw = (self.b_e_x - self.b_s_x)
        bh = (self.b_e_y - self.b_s_y)
        sw = min(screen_width, bw)
        sh = min(screen_height, bh)
        # Map width to screen width ratio
        m_s_w = bw / sw
        # Map height to screen height ratio
        m_s_h = bh / sh

        # Iterate over the screen width and height
        for sy in range(sh):
            for sx in range(sw):
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
            print '_',
        print ''


'''

m = Map(100, 100, 10)
for i in range(5):
    m.move(0, 4)
for i in range(5):
    m.move(90, 4)
for i in range(5):
    m.move(180, 4)
for i in range(5):
    m.move(270, 4)

for i in range(5):
    m.move(45, 10)
for i in range(5):
    m.move(135, 3)
for i in range(5):
    m.move(225, 3)

m.printMap(30, 60)

'''