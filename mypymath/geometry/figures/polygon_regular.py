import math

from mypymath.geometry.figures import Point, Plane


class PolygonRegular:
    """
    A special case of a polygon.

    """
    def __init__(self,
                 param1): # vertices
        self.name = 'polygon_regular'
        if isinstance(param1, tuple) or isinstance(param1, list):
            if len(param1) < 3:
                print('Error in Polygon.__init__:',
                      'vertives number < 3.')
                return None
            vertices = param1
        self.__init_primitive(vertices)

    def __init_primitive(self, vertices):
        self.vertices = vertices
        x = 0
        y = 0
        z = 0
        for pt in vertices:
            x += pt.x
            y += pt.y
            z += pt.z
        self.N = len(vertices)
        self.central_angle = 2 * math.pi / self.N
        self.center = Point(x / self.N, y / self.N, z / self.N)
        # TODO - check with help of DistanceCalculator
        #dc = DistanceCalculator()
        #self.edge_length = dc.distance(vertices[0], vertices[1])
        dx = vertices[1].x - vertices[0].x
        dy = vertices[1].y - vertices[0].y
        dz = vertices[1].z - vertices[0].z
        self.edge_length = (dx**2 + dy**2 + dz**2)**0.5
        self.outer_radius = self.edge_length / 2 / math.sin(self.central_angle / 2)
        self.inner_radius = (self.outer_radius**2 - self.edge_length**2 / 4)**0.5
        self.containing_plane = Plane(vertices[0], vertices[1], vertices[2])
        triangle_area = 0.5 * math.sin(self.central_angle) * self.outer_radius**2
        self.area = self.N * triangle_area

    def __str__(self, inside_other=False):
        if inside_other:
            result = '  '
        else:
            result = ''
        result += 'poly_reg[\n'
        for vertex in self.vertices:
            if inside_other:
                result += '  '
            result += '  ' + str(vertex) + '\n'
        result += ']'
        return result

    def translated(self, vector):
        return PolygonRegular([v.translated(vector) for v in self.vertices])
