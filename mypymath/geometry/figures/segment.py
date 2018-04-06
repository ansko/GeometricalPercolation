from mypymath.linalg.vector import Vector
from mypymath.geometry.figures import Point


class Segment:
    def __init__(self,
                 param1, param2=None, param3=None): # (vec, ANY, ANY) or 
                                                    # (x, y, z) or
                                                    # (pt, (pt or vec))
        """
        Prepare init params.

        """
        self.name = 'segment'
        if isinstance(param1, Vector):
            point1_x = 0
            point1_y = 0
            point1_z = 0
            point2_x = param1.x
            point2_y = param1.y
            point2_z = param1.z
            self.__init_primitive(point1_x, point1_y, point1_z,
                                  point2_x, point2_y, point2_z)
            return
        elif isinstance(param1, Point):
            point1_x = param1.x
            point1_y = param1.y
            point1_z = param1.z
        elif (isinstance(param1, (int, float)) and
              isinstance(param2, (int, float)) and
              isinstance(param3, (int, float))):
            point1_x = 0
            point1_y = 0
            point1_z = 0
            point2_x = float(param1)
            point2_y = float(param2)
            point2_z = float(param3)
            self.__init_primitive(point1_x, point1_y, point1_z,
                                  point2_x, point2_y, point2_z)
            return
        else:
            print('Error in Segment.__init__:',
                  'incorrect type of first argument')
            return None
        if isinstance(param2, Point) or isinstance(param2, Vector):
            point2_x = param2.x
            point2_y = param2.y
            point2_z = param2.z
        else:
            print('Error in Segment.__init__:',
                  'incorrect type of second argument')
            return None
        self.__init_primitive(point1_x, point1_y, point1_z,
                              point2_x, point2_y, point2_z)

    def __init_primitive(self, point1_x, point1_y, point1_z,
                               point2_x, point2_y, point2_z):
        """
        Init by prepared params.

        """
        self.begin = Point(point1_x, point1_y, point1_z)
        self.end = Point(point2_x, point2_y, point2_z)

    def __str__(self):
        return 'seg[' + str(self.begin) + ', ' + str(self.end) + ']'
    #
    # Some properties.
    #
    def length(self):
        dx = self.end.x - self.begin.x
        dy = self.end.y - self.begin.y
        dz = self.end.z - self.begin.z
        return (dx**2 + dy**2 + dz**2)**0.5
