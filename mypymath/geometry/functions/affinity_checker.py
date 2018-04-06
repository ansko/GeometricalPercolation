from mypymath.linalg import Vector, Matrix3

from mypymath.geometry.figures import (Point, Line, Segment, Plane, PolygonRegular,
                                       PrismRegular)
from mypymath.geometry.functions import Utility


class AffinityChecker:
    """
    Performs a checking whether primitive_in is
    ( !!!--- COMPLETELY ---!!! )
    inside of a primitive_out.
    The word affinity came frome translate.google.com's
    "affinity to a set" for russian "принадлежность множеству".
    """
    def __init__(self, epsilon=None): # epsilon is a desired accuracy
                                      # (0.001 by default)
        if epsilon is not None:
            self.epsilon = epsilon
        else:
            self.epsilon = 0.001
        self.checks = dict()
        self.checks['point'] = dict()
        pt_checks = self.checks['point']
        pt_checks['to_line'] = self.__checker_point_2line
        pt_checks['to_segment'] = self.__checker_point_2segment
        pt_checks['to_plane'] = self.__checker_point_2plane
        pt_checks['to_polygon_regular'] = self.__checker_point_2polygon
        pt_checks['to_polygon'] = self.__checker_point_2polygon
        pt_checks['to_prism_regular'] = self.__checker_point_2prism
        pt_checks['to_prism'] = self.__checker_point_2prism
        self.checks['line'] = dict()
        line_checks = self.checks['line'] 
        line_checks['to_plane'] = self.__checker_line_2plane
        self.checks['segment'] = dict()
        seg_checks = self.checks['segment']
        seg_checks['to_line'] = self.__checker_segment_2line
        seg_checks['to_segment'] = self.__checker_segment_2segment
        seg_checks['to_plane'] = self.__checker_segment_2plane
        seg_checks['to_polygon_regular'] = self.__checker_segment_2polygon
        seg_checks['to_polygon'] = self.__checker_segment_2polygon
        seg_checks['to_prism_regular'] = self.__checker_segment_2prism
        seg_checks['to_prism'] = self.__checker_segment_2prism
        self.checks['polygon'] = dict()
        poly_checks = self.checks['polygon']
        poly_checks['to_plane'] = self.__checker_polygon_2plane
        poly_checks['to_polygon_regular'] = self.__checker_polygon_2polygon
        poly_checks['to_polygon'] = self.__checker_polygon_2polygon
        poly_checks['to_prism_regular'] = self.__checker_polygon_2prism
        poly_checks['to_prism'] = self.__checker_polygon_2prism
        self.checks['polygon_regular'] = self.checks['polygon']
        self.checks['prism'] = dict()
        prism_checks = self.checks['prism']
        prism_checks['to_prism_regular'] = self.__checker_prism_2prism
        prism_checks['to_prism'] = self.__checker_prism_2prism
        self.checks['prism_regular'] = self.checks['prism']

    def check(self, primitive_in, primitive_out):
        """
        Choose and run proper method.

        """
        if isinstance(primitive_in, Point):
            name_in = 'point'
            if isinstance(primitive_out, (Line, Segment, Plane,
                                          PolygonRegular, PrismRegular)):
                 name_out = primitive_out.name
            else:
                print('Error in AffinityChecker.check:',
                      'some wrong type of outer primitive with inner Point.')
                return None
        elif isinstance(primitive_in, Line):
            name_in = 'line'
            if isinstance(primitive_out, Plane):
                name_out = 'plane'
            elif isinstance(primitive_out, (Segment,
                                            PolygonRegular, PrismRegular)):
                    # non-bonded primitive can not be inside bonded
                return False
            else:
                print('Error in AffinityChecker.check:',
                      'some wrong type of outer primitive with inner Line.')
                return None
        elif isinstance(primitive_in, Segment):
            name_in = 'segment'
            if isinstance(primitive_out, (Line, Segment, Plane,
                                          PolygonRegular, PrismRegular)):
                name_out = primitive_out.name
            else:
                print('Error in AffinityChecker.check:',
                      'some wrong type of outer primitive with inner Segment.')
                return None
        elif isinstance(primitive_in, PolygonRegular):
            name_in = 'polygon_regular'
            if isinstance(primitive_out, (Plane,
                                          PolygonRegular, PrismRegular)):
                name_out = primitive_out.name
            else:
                print('Error in AffinityChecker.check:',
                      'some wrong type of outer primitive with inner',
                      'PolygonRegular.')
                return None
        elif isinstance(primitive_in, PrismRegular):
            name_in = 'prism_regular'
            if isinstance(primitive_out, PrismRegular):
                name_out = 'prism_regular'
            else:
                print('Error in AffinityChecker.check:',
                      'some wrong type of outer primitive with inner',
                      'PrismRegular.')
                return None
        name_out = 'to_' + name_out
        return self.checks[name_in][name_out](primitive_in, primitive_out)

    def __checker_point_2line(self, point, line):
        """
        If th enequality of a triangle becomes to the equality
        then some point belongs to some segment consequently
        it belongs to line.
        """
        dx = line.parallel_vector.x
        dy = line.parallel_vector.y
        dz = line.parallel_vector.z
        ptdx = point.x - line.point1.x
        ptdy = point.y - line.point1.y
        ptdz = point.z - line.point1 .z
        if (abs(ptdx * dy - ptdy * dx) < self.epsilon and
            abs(ptdx * dz - ptdz * dx) < self.epsilon):
                return True
        return False

        pt1 = line.point1
        pt2 = line.point2
        dx1 = pt1.x - point.x
        dy1 = pt1.y - point.y
        dz1 = pt1.z - point.z
        length1 = (dx1**2 + dy1**2 + dz1**2)**0.5
        dx2 = pt2.x - point.x
        dy2 = pt2.y - point.y
        dz2 = pt2.z - point.z
        length2 = (dx2**2 + dy2**2 + dz2**2)**0.5
        length12 = line.parallel_vector.length()
        if min(abs(length12 - length1 - length2),
               abs(length1 - length12 - length2),
               abs(length2 - length12 - length1)) < self.epsilon:
            return True
        return False

    def __checker_point_2segment(self, point, segment):
        """
        If th enequality of a triangle becomes to the equality
        then point belongs to the segment.
        """
        pt1 = segment.begin
        pt2 = segment.end
        dx1 = pt1.x - point.x
        dy1 = pt1.y - point.y
        dz1 = pt1.z - point.z
        length1 = (dx1**2 + dy1**2 + dz1**2)**0.5
        dx2 = pt2.x - point.x
        dy2 = pt2.y - point.y
        dz2 = pt2.z - point.z
        length2 = (dx2**2 + dy2**2 + dz2**2)**0.5
        length12 = segment.length()
        if abs(length12 - length1 - length2) < self.epsilon:
            return True
        return False

    def __checker_point_2plane(self, point, plane):
        """
        Test whether the point corresponds to the plane's equation.

        """
        if abs(plane.a*point.x + plane.b*point.y +
               plane.c*point.z + plane.d) < self.epsilon:
            return True
        return False

    def __checker_point_2polygon(self, point, polygon):
         """
         Firstly check whether point is in polygon's plane.
         After that check whether the sum of triangles
         (formed by point and polygon's edges) equals to
         the area of a polygon.

         """
         if not self.__checker_point_2plane(point, polygon.containing_plane):
             pl = polygon.containing_plane
             return False
         polygon_area = polygon.area 
         triangles_area = 0
         for i, vertex1 in enumerate(polygon.vertices):
             vertex2 = polygon.vertices[i - 1]
             triangles_area += Utility().triangle_area(point, vertex1, vertex2)
         if abs(triangles_area - polygon_area) < self.epsilon:
             return True
         return False

    def __checker_point_2prism(self, point, prism):
        """
        Check whether volume of prism equlas to the sum of volumes
        of pyramides composed by point and prism's facets.
        """
        prism_volume = prism.height * prism.top_facet.area
        pyramides_volume = 0
        # top and bottom facets
        vec1 = Vector(point, prism.top_facet.vertices[0])
        vec2 = Vector(point, prism.top_facet.vertices[1])
        vec3 = Vector(point, prism.top_facet.vertices[2])
        vec4 = Vector(point, prism.top_facet.vertices[3])
        elements = [vec1.x, vec1.y, vec1.z,
                    vec2.x, vec2.y, vec2.z,
                    vec3.x, vec3.y, vec3.z]
        pyramides_volume += abs(1/6 * Matrix3(elements).det())
        elements = [vec1.x, vec1.y, vec1.z,
                    vec3.x, vec3.y, vec3.z,
                    vec4.x, vec4.y, vec4.z]
        pyramides_volume += abs(1/6 * Matrix3(elements).det())
        vec1 = Vector(point, prism.bottom_facet.vertices[0])
        vec2 = Vector(point, prism.bottom_facet.vertices[1])
        vec3 = Vector(point, prism.bottom_facet.vertices[2])
        vec4 = Vector(point, prism.bottom_facet.vertices[3])
        elements = [vec1.x, vec1.y, vec1.z,
                    vec2.x, vec2.y, vec2.z,
                    vec3.x, vec3.y, vec3.z]
        pyramides_volume += abs(1/6 * Matrix3(elements).det())
        elements = [vec1.x, vec1.y, vec1.z,
                    vec3.x, vec3.y, vec3.z,
                    vec4.x, vec4.y, vec4.z]
        pyramides_volume += abs(1/6 * Matrix3(elements).det())
        # side facets
        for i in range(len(prism.top_facet.vertices)):
            vec1 = Vector(point, prism.top_facet.vertices[i])
            vec2 = Vector(point, prism.top_facet.vertices[i - 1])
            vec3 = Vector(point, prism.bottom_facet.vertices[i - 1])
            vec4 = Vector(point, prism.bottom_facet.vertices[i])
            elements = [vec1.x, vec1.y, vec1.z,
                        vec2.x, vec2.y, vec2.z,
                        vec3.x, vec3.y, vec3.z]
            pyramides_volume += abs(1/6 * Matrix3(elements).det())
            elements = [vec1.x, vec1.y, vec1.z,
                        vec3.x, vec3.y, vec3.z,
                        vec4.x, vec4.y, vec4.z]
            pyramides_volume += abs(1/6 * Matrix3(elements).det())
        if abs(prism_volume - pyramides_volume) < self.epsilon:
            return True
        return False

    def __checker_line_2plane(self, line, plane):
        return (self.__checker_point_2plane(line.point1, plane) and
                self.__checker_point_2plane(line.point2, plane))

    def __checker_segment_2line(self, segment, line):
        return (self.__checker_point_2line(segment.begin, line) and
                self.__checker_point_2line(segment.end, line))

    def __checker_segment_2segment(self, segment_in, segment_out):
        return (self.__checker_point_2segment(segment_in.begin, segment_out) and
                self.__checker_point_2segment(segment_in.end, segment_out))

    def __checker_segment_2plane(self, segment, plane):
        return (self.__checker_point_2plane(segment.begin, plane) and
                self.__checker_point_2plane(segment.end, plane))

    def __checker_segment_2polygon(self, segment, polygon):
        return (self.__checker_point_2polygon(segment.begin, polygon) and
                self.__checker_point_2polygon(segment.end, polygon))

    def __checker_segment_2prism(self, segment, prism):
        return (self.__checker_point_2prism(segment.begin, prism) and
                self.__checker_point_2prism(segment.end, prism))

    def __checker_polygon_2plane(self, polygon, plane):
        for vertex in polygon.vertices:
            if not self.__checker_point_2plane(vertex, plane):
                return False
        return True

    def __checker_polygon_2polygon(self, polygon_in, polygon_out):
        for vertex in polygon_in.vertices:
            if not self.__checker_point_2polygon(vertex, polygon_out):
                return False
        return True

    def __checker_polygon_2prism(self, polygon, prism):
        for vertex in polygon.vertices:
            if not self.__checker_point_2prism(vertex, prism):
                return False
        return True

    def __checker_prism_2prism(self, prism_in, prism_out):
        for vertex in prism_in.top_facet.vertices:
            if not self.__checker_point_2prism(vertex, prism_out):
                return False
        for vertex in prism_in.bottom_facet.vertices:
            if not self.__checker_point_2prism(vertex, prism_out):
                return False
        return True
