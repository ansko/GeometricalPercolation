from mypymath.linalg.vector import Vector
from mypymath.geometry.figures import Point, Segment

class Line:
    """
    Line may be set by two given points.
    vec is a vector parallel to line, it is useful in many algorythms
    """
    def __init__(self,
                 param1, param2=None): # (seg or vec, ANYTHING) or
                                       # (pt, (pt or vec))
        """
        Prepare init params.

        """
        self.name = 'line'
        if isinstance(param1, Segment):
            point1_x = param1.begin.x
            point1_y = param1.begin.y
            point1_z = param1.begin.z
            point2_x = param1.end.x
            point2_y = param1.end.y
            point2_z = param1.end.z
            self.__init_primitive(point1_x, point1_y, point1_z,
                                  point2_x, point2_y, point2_z)
            return
        elif isinstance(param1, Vector):
            point1_x = 0
            point1_y = 0
            point1_z = 0
            point2_x = param1.x
            point2_y = param1.y
            point2_z = param1.z
        elif isinstance(param1, Point):
            point1_x = param1.x
            point1_y = param1.y
            point1_z = param1.z
        else:
            print('Error in Line.__init__:',
                  'param1 is not a Point type')
            return None
        if isinstance(param2, Point):
            point2_x = param2.x
            point2_y = param2.y
            point2_z = param2.z
        elif isinstance(param2, Vector):
            point2_x = point1_x + param2.x
            point2_y = point1_y + param2.y
            point2_z = point1_z + param2.z
        else:
            print('Error in Line.__init__:',
                  'param2 is not a Point or Vector type')
            return None
        self.__init_primitive(point1_x, point1_y, point1_z,
                              point2_x, point2_y, point2_z)

    def __init_primitive(self, point1_x, point1_y, point1_z,
                               point2_x, point2_y, point2_z):
        """
        Init by prepared params.

        """
        self.point1 = Point(point1_x, point1_y, point1_z)
        self.point2 = Point(point2_x, point2_y, point2_z)
        dx = point2_x - point1_x
        dy = point2_y - point1_y
        dz = point2_z - point1_z
        self.parallel_vector = Vector(dx, dy, dz)

    def __str__(self):
        return 'line[' + str(self.point1) + ', ' + str(self.parallel_vector) + ']'
