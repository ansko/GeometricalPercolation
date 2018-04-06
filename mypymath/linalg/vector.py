class Vector:
    def __init__(self,
                 param1, param2=None, param3=None): # I have to use another way
                                                    # than in geometry primitives,
                                                    # becuase i don't want to make
                                                    # vector dependant from
                                                    # geometry primitives.
                                                    # TODO - implement better.
        if param1 is not None and param2 is None and param3 is None:
            # Init by segment.
            try:
                x = float(param1.end.x - param1.begin.x)
                y = float(param1.end.y - param1.begin.y)
                z = float(param1.end.z - param1.begin.z)
            except:
                print('Error in Vector.__init__:',
                      'incorrect type of input arguments')
                return None
        elif param1 is not None and param2 is not None and param3 is None:
            # Init by 2 points.
            try:
                x = float(param2.x - param1.x)
                y = float(param2.y - param1.y)
                z = float(param2.z - param1.z)
            except:
                print('Error in Vector.__init__:',
                      'incorrect type of input arguments')
                return None
        elif param1 is not None and param2 is not None and param3 is not None:
            # Init by 3 coordinates.
            try:
                x = float(param1)
                y = float(param2)
                z = float(param3)
            except:
                print('Error in Vector.__init__:',
                      'incorrect type of input arguments')
                return None
        else:
            print('Error in Vector.__init__:',
                  'incorrect type of input arguments.')
            return None
        self.__init_entity(x, y, z)
        return

    def __init_entity(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    """
        Other special methods.
    """
    def __str__(self):
        return 'vec(' + str(self.x) + ', ' + str(self.y) + '. ' + str(self.z) + ')'

    def __neg__(self):
        return Vector(-self.x, -self.y, -self.z)


    """
        A group of methods to get vector's properties.
    """
    def length(self):
        return (self.x**2 + self.y**2 + self.z**2)**0.5

    def product_with(self, vec):
        return self.x * vec.x + self.y * vec.y + self.z * vec.z

    def vector_product_with(self, vec):
        x = self.y * vec.z - self.z * vec.y
        y = -self.x * vec.z + self.z * vec.x
        z = self.x * vec.y - self.y * vec.x
        return Vector(x=x, y=y, z=z)

    """
        A group of methods to change self.
    """
    def multiply_by_number(self, number, debug_flag=False):
        if number == 0 and debug_flag:
            print('warning:',
                  'vector multiply_by_number: number is 0!')
        self.x *= number
        self.y *= number
        self.z *= number

    def divide_by_number(self, number):
        if number == 0:
            print('error:',
                  'vector divide_by_number: number is 0!')
            return None
        self.x /= number
        self.y /= number
        self.z /= number

    def add_vector(self, vector):
        self.x += vector.x
        self.y += vector.y
        self.z += vector.z

    def substract_vector(self, vector):
        self.x -= vector.x
        self.y -= vector.y
        self.z -= vector.z

    def renorm(self, length=1):
        """
            Make self having given length.
        """
        self.multiply_by_number(length / self.length())
