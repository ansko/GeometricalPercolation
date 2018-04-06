from mypymath.linalg.vector import Vector
from mypymath.linalg.matrix3 import Matrix3
from mypymath.geometry.figures import Point, Line, Segment


class Plane:
    """
    Represents a plane:
    a*x + b*y + c*z + d = 0
    """
    def __init__(self,
                 param1, param2, param3=None, param4=None): # (a, b, c, d) or
                                                            # --- 3 pts ---
                                                            # (pt1, pt2, pt3) or
                                                            # (pt, vec) or
                                                            # --- 4 pts ---
                                                            # (vec, vec) or
                                                            # (seg, seg) or
                                                            # (line, line)
        self.name = 'plane'
        if (isinstance(param1, (float, int)) and
                isinstance(param2, (float, int)) and
                isinstance(param3, (float, int)) and
                isinstance(param4, (float, int))):
            #Init directly by a, b, c, d
            a = param1
            b = param2
            c = param3
            d = param4
            self.__init_primitive(a, b, c, d)
            return
        elif isinstance(param1, Point):
            point1_x = param1.x
            point1_y = param1.y
            point1_z = param1.z
            if isinstance(param2, Vector):
                # Init by point and normal
                normal_x = param2.x
                normal_y = param2.y
                normal_z = param2.z
                a = normal_x
                b = normal_y
                c = normal_z
                d = -point1_x*a - point1_y*b - point1_z*c
            elif isinstance(param2, Point) and isinstance(param3, Point):
                point1 = param1
                point2 = param2
                point3 = param3
                self.__init_three_points(point1, point2, point3)
                return
        elif (isinstance(param1, (Segment, Vector, Line)) and
              isinstance(param2, (Segment, Vector, Line))):
            try:
                # segment
                point1 = param1.begin
                point2 = param1.end
            except:
                try:
                    # line
                    point1 = param1.point1
                    point2 = param1.point2
                except:
                    # vector
                    point1 = Point(0, 0, 0)
                    point2 = Point(param1)
            try:
                # segment
                point3 = param2.begin
                point4 = param2.end
            except:
                try:
                    # line
                    point3 = param2.point1
                    point4 = param2.point2
                except:
                    # vector
                    point3 = Point(0, 0, 0)
                    point4 = Point(param2)
            #
            # Check whether four points are in single plane
            # by calculating det (vec12, vec13, vec14)
            # which is proportional to the tetrahedra volume
            # with vertices in points 1, 2, 3 and 4.
            # After that it is possible to call __init_three_points
            # with any 3 of these 4 points
            # (i've chosen points 1, 2 and 4).
            # becaues in case of 2 vectors pt1 == pt3,
            # so they are at a single line.
            #
            elements = [point2.x - point1.x,
                        point2.y - point1.y,
                        point2.z - point1.z,
                        point3.x - point1.x,
                        point3.y - point1.y,
                        point3.z - point1.z,
                        point4.x - point1.x,
                        point4.y - point1.y,
                        point4.z - point1.z]
            if Matrix3(elements=elements).det() == 0:
                self.__init_three_points(point1, point2, point4)
            else:
                print('Error in Plane.__init__:',
                      'there are 4 points that do not lie in a single plane')
                return None
            return
        else:
            print('Error in Plane.__init__:',
                  'incorrect type of some argument')
            return None
        self.__init_primitive(a, b, c, d)

    def __init_primitive(self, a, b, c, d):
        """
        Init by prepared params.

        """
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def __init_three_points(self, point1, point2, point3):
        """
        Calls __init_primitive(a, b, c, d)
        after performing calculation of  a, b, c and d
        using three points' coordinates.

        """
        minor_x = ((point2.y - point1.y) * (point3.z - point1.z) -
                   (point3.y - point1.y) * (point2.z - point1.z))
        minor_y = ((point2.x - point1.x) * (point3.z - point1.z) -
                   (point3.x - point1.x) * (point2.z - point1.z))
        minor_z = ((point2.x - point1.x) * (point3.y - point1.y) -
                   (point2.y - point1.y) * (point3.x - point1.x))
        if minor_x == 0 and minor_y == 0 and minor_z == 0:
            print('Error in Plane.__init__:',
                  '3 points lie on a single line')
            return None
        elif minor_x == 0 and minor_y == 0:
            a = 0
            b = 0
            c = 1
            d = -point1.z
        elif minor_x == 0 and minor_z == 0:
            a = 0
            b = 1
            c = 0
            d = -point1.y
        elif minor_y == 0 and minor_z == 0:
            a = 1
            b = 0
            c = 0
            d = -point1.x
        elif minor_x == 0:
            a = 0
            b = minor_y
            c = minor_z
            d = -point1.y*minor_y - minor_z*point1.z
        elif minor_y == 0:
            a = minor_x
            b = 0
            c = minor_z
            d = -point1.x*minor_x - minor_z*point1.z
        elif minor_z == 0:
            a = minor_x
            b = minor_y
            c = 0
            d = -point1.x*minor_x - minor_y*point1.y
        else:
            a = minor_x
            b = minor_y
            c = minor_z
            d = -point1.x*minor_x - minor_y*point1.y - minor_z*point1.z
        self.__init_primitive(a, b, c, d)
        return

    def __str__(self):
        return ('plane(' + str(self.a) +
                    ', ' + str(self.b) +
                    ', ' + str(self.c) +
                    ', ' + str(self.d) + ')')

    def get_point_sign(self, point):
        value = self.a*point.x + self.b*point.y + self.c*point.z + self.d
        if value == 0:
            return 0
        return value / abs(value)
