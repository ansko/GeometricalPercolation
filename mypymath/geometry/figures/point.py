from mypymath.linalg.vector import Vector

class Point:
    def __init__(self,
                 param1, param2=None, param3=None): # (pt or vec, ANY, ANY) or
                                                    # (x, y, z)
        """
        Prepare init params.

        """
        self.name = 'point'
        if isinstance(param1, Point) or isinstance(param1, Vector):
            point_x = param1.x
            point_y = param1.y
            point_z = param1.z
        elif (isinstance(param1, (float, int)) and
              isinstance(param2, (float, int)) and
              isinstance(param3, (float, int))):
            point_x = float(param1)
            point_y = float(param2)
            point_z = float(param3)
        else:
            print('Error in Point.__init__:',
                  'param1 is not Point or Vector or float type')
            return None
        self.__init_primitive(point_x, point_y, point_z)

    def __init_primitive(self, point_x, point_y, point_z):
        """
        Init by prepared params.

        """
        self.x = point_x
        self.y = point_y
        self.z = point_z

    def __str__(self):
        return ('pt(' + str(self.x) +
                 ', ' + str(self.y) +
                 ', ' + str(self.z) + ')')


    def translate(self, vector):
        self.x += vector.x
        self.y += vector.y
        self.z += vector.z


    def translated(self, vector):
        return Point(self.x + vector.x, self.y + vector.y, self.z + vector.z)
