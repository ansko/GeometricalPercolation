"""
https://app.gotowebinar.com/index.html#871432971/8853746303466369027/5967531579705068301
"""


from mypymath.linalg import Vector, Matrix2

from mypymath.geometry.figures import (Point, Line, Segment, Plane, PolygonRegular,
                                       PrismRegular)
from mypymath.geometry.functions import AffinityChecker

class DistanceCalculator:
    """
    The class is made to calculate the distance
    between two given figures.

    """
    def __init__(self, epsilon=None):
        """
        Init constructs a dict of methods.
        They are easy to call.
        """
        if epsilon is not None:
            self.epsilon = epsilon
        else:
            self.epsilon = 0.001
        self.methods = dict()
        self.methods['point'] = dict()
        pt_dist = self.methods['point']
        pt_dist['point'] = self.__distance_point_point
        pt_dist['line'] = self.__distance_point_line
        pt_dist['segment'] = self.__distance_point_segment
        pt_dist['plane'] = self.__distance_point_plane
        pt_dist['polygon_regular'] = self.__distance_point_polygon
        pt_dist['polygon'] = self.__distance_point_polygon
        pt_dist['prism_regular'] = self.__distance_point_prism
        pt_dist['prism'] = self.__distance_point_prism
        self.methods['line'] = dict()
        line_dist = self.methods['line']
        line_dist['point'] = self.__distance_line_point
        line_dist['line'] = self.__distance_line_line
        line_dist['segment'] = self.__distance_line_segment
        line_dist['plane'] = self.__distance_line_plane
        line_dist['polygon_regular'] = self.__distance_line_polygon
        line_dist['polygon'] = self.__distance_line_polygon
        line_dist['prism_regular'] = self.__distance_line_prism
        line_dist['prism'] = self.__distance_line_prism
        self.methods['segment'] = dict()
        sef_dist = self.methods['segment']
        sef_dist['point'] = self.__distance_segment_point
        sef_dist['line'] = self.__distance_segment_line
        sef_dist['segment'] = self.__distance_segment_segment
        sef_dist['plane'] = self.__distance_segment_plane
        sef_dist['polygon_regular'] = self.__distance_segment_polygon
        sef_dist['polygon'] = self.__distance_segment_polygon
        sef_dist['prism_regular'] = self.__distance_segment_prism
        sef_dist['prism'] = self.__distance_segment_prism
        self.methods['plane'] = dict()
        plane_dist = self.methods['plane']
        plane_dist['point'] = self.__distance_plane_point
        plane_dist['line'] = self.__distance_plane_line
        plane_dist['segment'] = self.__distance_plane_segment
        plane_dist['plane'] = self.__distance_plane_plane
        plane_dist['polygon_regular'] = self.__distance_plane_polygon
        plane_dist['polygon'] = self.__distance_plane_polygon
        plane_dist['prism_regular'] = self.__distance_plane_prism
        plane_dist['prism'] = self.__distance_plane_prism
        self.methods['polygon'] = dict()
        poly_dist = self.methods['polygon']
        poly_dist['point'] = self.__distance_polygon_point
        poly_dist['line'] = self.__distance_polygon_line
        poly_dist['segment'] = self.__distance_polygon_segment
        poly_dist['plane'] = self.__distance_polygon_plane
        poly_dist['polygon_regular'] = self.__distance_polygon_polygon
        poly_dist['polygon'] = self.__distance_polygon_polygon
        poly_dist['prism_regular'] = self.__distance_polygon_prism
        poly_dist['prism'] = self.__distance_polygon_prism
        self.methods['polygon_regular'] = self.methods['polygon']
        self.methods['prism'] = dict()
        prism_dist = self.methods['prism']
        prism_dist['point'] = self.__distance_prism_point
        prism_dist['line'] = self.__distance_prism_line
        prism_dist['segment'] = self.__distance_prism_segment
        prism_dist['plane'] = self.__distance_prism_plane
        prism_dist['polygon_regular'] = self.__distance_prism_polygon
        prism_dist['polygon'] = self.__distance_prism_polygon
        prism_dist['prism_regular'] = self.__distance_prism_prism
        prism_dist['prism'] = self.__distance_prism_prism
        self.methods['prism_regular'] = self.methods['prism']


    def distance(self, primitive1, primitive2):
        """
        Defines types of primitive1 and primitive2.
        After that calls proper specialized method.
        """
        # define primitives type
        if isinstance(primitive1, Point):
            name1 = 'point'
        elif isinstance(primitive1, Line):
            name1 = 'line'
        elif isinstance(primitive1, Segment):
            name1 = 'segment'
        elif isinstance(primitive1, Plane):
            name1 = 'plane'
        elif isinstance(primitive1, PolygonRegular):
            name1 = 'polygon'
        elif isinstance(primitive1, PrismRegular):
            name1 = 'prism'
        if isinstance(primitive2, Point):
            name2 = 'point'
        elif isinstance(primitive2, Line):
            name2 = 'line'
        elif isinstance(primitive2, Segment):
            name2 = 'segment'
        elif isinstance(primitive2, Plane):
            name2 = 'plane'
        elif isinstance(primitive2, PolygonRegular):
            name2 = 'polygon'
        elif isinstance(primitive2, PrismRegular):
            name2 = 'prism'
        # call proper method
        return self.methods[name1][name2](primitive1, primitive2)


    ################################################################
    #                                                              #
    # Implementation of specialized methods                        #
    # to calculate distance between two primitives.                #
    #                                                              #
    ################################################################


    def __distance_point_point(self, point1, point2):
        dx = point2.x - point1.x
        dy = point2.y - point1.y
        dz = point2.z - point1.z
        return (dx**2 + dy**2 + dz**2)**0.5

    def __distance_point_line(self, point, line):
        """
            pt0, pt1, pt2 form a triangle where
                pt0 = point,
                pt1 = line origin,
                pt2 = line origin + parallel_vector
            Firstly calculate triangle's square as 1/2 * v01 * v02 * sin(a102),
                where a102 is angle between v01 and v02,
                      v01 is vector from pt0 to pt1,
                      v02 is vector from pt0 to pt2.
            Then as 1/2 * h * v12.length()
                where h is height from pt0 to the segment connecting pt1 and pt2
                (the same as line.parallel_vector).
            Equating them one can find h.
        """
        pt0 = point
        pt1 = line.point1
        pt2 = line.point2
        line_parallel_vector_length = self.__distance_point_point(pt1, pt2)
        v01 = Vector(pt0, pt1)
        v02 = Vector(pt0, pt2)
        cos_angle_v01_v02 = v01.product_with(v02) / v01.length() / v02.length()
        sin_angle_v01_v02 = (1 - cos_angle_v01_v02**2)**0.5
        double_area = v01.length() * v02.length() * sin_angle_v01_v02
        if double_area == 0:
            return 0
        triangle_height = double_area / line_parallel_vector_length
        return triangle_height

    def __distance_point_segment(self, point, segment):
        """
            Consider here triangle made by point and segment.
            If there is any angle >= 90 degrees the distance is equal to the length
            of the edge lying near this angle. Otherwise the distance is equal to
            the height of the triangle.
        """
        pt0 = point
        pt1 = segment.begin
        pt2 = segment.end
        v01 = Vector(pt0, pt1)
        v02 = Vector(pt0, pt2)
        v12 = Vector(pt1, pt2)
        if v01.product_with(v12) >= 0:
            return v01.length()
        elif v02.product_with(v12) <= 0:
            return v02.length()
        height = self.__distance_point_line(point, Line(pt1, pt2))
        return height

    def __distance_point_plane(self, point, plane):
        """
             Find plane containing point and parallel to plane.
             Difference in d values is equal to the desired distance.
        """
        d = -point.x * plane.a - point.y * plane.b - point.z * plane.c
        return abs(plane.d - d)

    def __distance_point_polygon(self, point, polygon):
        """
            Find the distance to the plane containing polygon.
            If it equals zero then desired distance equals to the smallest of
            the distances to the polygon's edges.
            Otherwise, firstly, check whether the desired distance equals to the
            distance to the plane containing poly. It happens if the prism
            with top and bot equal to the poly translated to the vector vec,
            which is perpendicular to poly and has length equal to the distance to
            the plane, contains point.
            Otherwise the distance to the polygon is found by Pythagoras theorem:
            a = the smallest of the diatances to the segments forming prisms's
                top and bottom
            b = distance to the plane containing polygon
            c = (a**2 + b**2)**0.5 - distance of interest
        """
        ac = AffinityChecker()
        distance_to_plane = self.__distance_point_plane(point,
                                                        polygon.containing_plane)
        if distance_to_plane < self.epsilon:
            return self.__distance_point_polygon_edge(point, polygon)
        vec_to_plane = Vector(polygon.containing_plane.a,
                              polygon.containing_plane.b,
                              polygon.containing_plane.c)
        vec_to_plane.renorm(distance_to_plane)
        if not ac.check(point, PrismRegular(polygon.translated(vec_to_plane),
                                            polygon.translated(-vec_to_plane))):
            return self.__distance_point_polygon_edge(point, polygon)
        return distance_to_plane

    def __distance_point_polygon_edge(self, point, polygon):
        """
        Method to get minimal from distances
        from the point to the polygon's edges.
        """
        # start from the ("minus first" == last) edge
        segment = Segment(polygon.vertices[0], polygon.vertices[-1])
        min_distance_to_edge = self.__distance_point_segment(point, segment)
        for i in range(1, len(polygon.vertices)):
            segment = Segment(polygon.vertices[i], polygon.vertices[i - 1])
            current_distance_to_edge = self.__distance_point_segment(point,
                                                                     segment)
            min_distance_to_edge = min(min_distance_to_edge,
                                       current_distance_to_edge)
        return min_distance_to_edge

    def __distance_point_prism(self, point, prism):
        ac = AffinityChecker()
        if ac.check(point, prism):
            return 0
        dist_poly = self.__distance_point_polygon
        min_distance_to_facet = min(dist_poly(point, prism.top_facet),
                                    dist_poly(point, prism.bottom_facet))
        for i in range(len(prism.top_facet.vertices)):
            if i == 0:
                j = len(prism.top_facet.vertices) - 1
            else:
                j = i - 1
            side_facet = PolygonRegular([prism.top_facet.vertices[i],
                                         prism.top_facet.vertices[j],
                                         prism.bottom_facet.vertices[j],
                                         prism.bottom_facet.vertices[i]])
            min_distance_to_facet = min(min_distance_to_facet,
                                        dist_poly(point, side_facet))
        return min_distance_to_facet
        return -100

    def __distance_line_point(self, line, point):
        return self.__distance_point_line(point, line)

    def __distance_line_line(self, line1, line2):
        ptA = line1.point1
        ptB = line1.point2
        ptC = line2.point1
        ptD = line2.point2
        vecAB = Vector(ptA, ptB)
        vecCD = Vector(ptC, ptD)
        # check if these lines are parallel
        param = abs(vecAB.product_with(vecCD) / vecAB.length() / vecCD.length())
        if param - 1 < self.epsilon:
            vecAD = Vector(ptA, ptD)
            if vecAD.length() == 0:
                return 0
            cos_angle_A = (vecAD.product_with(vecAB) /
                           vecAB.length() /
                           vecAD.length())
            sin_angle_A = (1 - cos_angle_A**2)**0.5
            return vecAD.length() * sin_angle_A
        # lines are not parallel
        c11 = -vecAB.length()**2
        c12 = vecAB.product_with(vecCD)
        c22 = vecCD.length()**2
        # tmp vector for easy calculation procedure
        vecBETA = Vector(ptC.x - ptA.x, ptC.y - ptA.y, ptC.z - ptA.z)
        b1 = -vecBETA.product_with(vecAB)
        b2 = -vecBETA.product_with(vecCD)
        """
            System to solve is:
            |c11  c12 | b1 |
            |-c12 c22 | b2 |
        """
        det = c11*c22 + c12**2
        if det == 0:
            # Line AB and line CD cross.
            return 0
        det_alpha = b1*c22 - b2*c12
        det_gamma = c11*b2 + c12*b1
        alpha = det_alpha / det
        gamma = det_gamma / det
        vecAB.multiply_by_number(alpha)
        ptE = ptA.translated(vecAB)
        vecCD.multiply_by_number(gamma)
        ptF = ptC.translated(vecCD)
        return Vector(ptE, ptF).length()

    def __distance_line_segment(self, line, segment):
        ptA = line.point1
        ptB = line.point2
        ptC = segment.begin
        ptD = segment.end
        vecAB = Vector(ptA, ptB)
        vecCD = Vector(ptC, ptD)
        # check if these lines are parallel
        param = abs(vecAB.product_with(vecCD) / vecAB.length() / vecCD.length())
        if param - 1 < self.epsilon:
            vecAD = Vector(ptA, ptD)
            if vecAD.length() == 0:
                return 0
            cos_angle_A = (vecAD.product_with(vecAB) /
                           vecAB.length() /
                           vecAD.length())
            sin_angle_A = (1 - cos_angle_A**2)**0.5
            return vecAD.length() * sin_angle_A
        # lines are not parallel
        c11 = -vecAB.length()**2
        c12 = vecAB.product_with(vecCD)
        c22 = vecCD.length()**2
        # tmp vector for easy calculation procedure
        vecBETA = Vector(ptC.x - ptA.x, ptC.y - ptA.y, ptC.z - ptA.z)
        b1 = -vecBETA.product_with(vecAB)
        b2 = -vecBETA.product_with(vecCD)
        """
            System to solve is:
            |c11  c12 | b1 |
            |-c12 c22 | b2 |
        """
        det = c11*c22 + c12**2
        if det == 0:
            # Line AB and line CD cross.
            return 0
        det_alpha = b1*c22 - b2*c12
        det_gamma = c11*b2 + c12*b1
        alpha = det_alpha / det
        gamma = det_gamma / det
        vecAB.multiply_by_number(alpha)
        ptE = ptA.translated(vecAB)
        vecCD.multiply_by_number(gamma)
        if 0 <= gamma <= 1:
            ptF = ptC.translated(vecCD)
        elif gamma < 0:
            ptF = ptC
        else:
            ptF = ptD
        return Vector(ptE, ptF).length()

    def __distance_line_plane(self, line, plane):
        normal_to_plane = Vector(plane.a, plane.b, plane.c)
        # Check if they are parallel;
        # otherwise they surely cross.
        if line.parallel_vector.product_with(normal_to_plane) > self.epsilon:
            return 0
        # Distances from all line points to plane are equal.
        return self.__distance_point_plane(line.point1, plane)

    def __distance_line_polygon(self, line, polygon):
        distance = self.__distance_line_segment
        edge = Segment(polygon.vertices[0], polygon.vertices[-1])
        # start value
        min_distance_to_edge = distance(line, edge)
        for i in range(1, len(polygon.vertices)):
            edge = Segment(polygon.vertices[i], polygon.vertices[i - 1])
            min_distance_to_edge = min(min_distance_to_edge,
                                       distance(line, edge))
        pl = polygon.containing_plane
        vec = line.parallel_vector
        pt = line.point1
        if self.__distance_line_plane(line, pl) != 0:
            return min_distance_to_edge
        #ptCross = point1 + alpha*parallel_vector
        alpha = ((-pl.a*pt.x - pl.b*pt.y - pl.c*pt.z - pl.d) /
                 (vec.x + vec.y + vec.z))
        ptCross = Point(pt.x + alpha*vec.x,
                        pt.y + alpha*vec.y,
                        pt.z + alpha*vec.z)
        ac = AffinityChecker()
        if ac.check(ptCross, polygon):
            return 0
        return min_distance_to_edge

    def __distance_line_prism(self, line, prism):
        distance = self.__distance_line_polygon
        min_facet_distance = min(distance(line, prism.top_facet),
                                 distance(line, prism.bottom_facet))
        for i in range(len(prism.top_facet.vertices)):
            if i == 0:
                j = len(prism.top_facet.vertices) - 1
            else:
                j = i - 1
            side_facet = PolygonRegular([prism.top_facet.vertices[i],
                                         prism.bottom_facet.vertices[i],
                                         prism.bottom_facet.vertices[j],
                                         prism.top_facet.vertices[j]])
            tmp_distance = distance(line, side_facet)
            min_facet_distance = min(min_facet_distance, tmp_distance)
        return min_facet_distance

    def __distance_segment_point(self, segment, point):
        return self.__distance_point_segment(point, segment)

    def __distance_segment_line(self, segment, line):
        return self.__distance_line_segment(line, segment)

    def __distance_segment_segment(self, segment1, segment2):
        ptA = segment1.begin
        ptB = segment1.end
        ptC = segment2.begin
        ptD = segment2.end
        vecAB = Vector(ptA, ptB)
        vecCD = Vector(ptC, ptD)
        vecAC = Vector(ptA, ptC)
        vecBD = Vector(ptB, ptD)
        vecBC = Vector(ptB, ptC)
        vecAD = Vector(ptA, ptD)
        if (vecAC.length() == 0 or
            vecAD.length() == 0 or
            vecBD.length() == 0 or
            vecBD.length() == 0):
                return 0
        cos_AB_CD = vecAB.product_with(vecCD) / vecAB.length() / vecCD.length()
        if abs(abs(cos_AB_CD) - 1) < self.epsilon:
            # parallel or at one line
            cos_BAC = vecAB.product_with(vecAC) / vecAB.length() / vecAC.length()
            cos_ABD = vecAB.product_with(vecBD) / vecAB.length() / vecBD.length()
            if (abs(abs(cos_BAC) - 1) < self.epsilon and
                abs(abs(cos_ABD) - 1) < self.epsilon):
                # lie on one line
                ac = AffinityChecker()
                if (ac.check(ptA, segment2) or ac.check(ptB, segment2) or
                    ac.check(ptC, segment1) or ac.check(ptD, segment1)):
                    # vectors cross
                    return 0
                return min(vecAD.length(),
                           vecAC.length(),
                           vecBD.length(),
                           vecBC.length())
            if abs(abs(cos_BAC) - 1) < self.epsilon:
                # ptC belongs to line AB, ptD does not
                return min(vecBC.length(), vecAC.length())
            if abs(abs(cos_ABD) - 1) < self.epsilon:
                # ptD belongs to line AB, ptC does not
                return min(vecAD.length(), vecBD.length())
            distance = self.__distance_point_segment
            return min(distance(ptA, segment2),
                       distance(ptB, segment2),
                       distance(ptC, segment1),
                       distance(ptD, segment1))
        # lines are not parallel
        c11 = -vecAB.length()**2
        c12 = vecAB.product_with(vecCD)
        c22 = vecCD.length()**2
        # tmp vector for easy calculation procedure
        b1 = -vecAC.product_with(vecAB)
        b2 = -vecAC.product_with(vecCD)
        """
            System to solve is:
            |c11  c12 | b1 |
            |-c12 c22 | b2 |
        """
        det = c11*c22 + c12**2
        if det == 0:
            # Line AB and line CD cross (?)
            # ptCross = ptA + fi * vecAB == ptC + xi * vecCD
            d = Matrix2([-vecAD.x, vecCD.x,
                         -vecAB.y, vecCD.y]).det()
            dfi = Matrix2([ptC.x - ptA.x, vecCD.x,
                           ptC.y - ptA.y, vecCD.y]).det()
            dxi = Matrix2([-vecAB.x, ptC.x - ptA.x,
                           -vecAB.y, ptC.y - ptA.y]).det()
            if d == 0:
                # cross of segments (?)
                return 0
            else:
                fi = dfi / d
                xi = dxi / d
                if fi < 0 : 
                    ptE = ptA
                elif fi > 1:
                    ptE = ptB
                else:
                    vecAB.multiply_by_number(fi)
                    ptE = ptA.translated(vecAB)
                if xi < 0:
                    ptF = ptC
                elif xi > 1:
                    ptF = ptD
                else:
                    vecCD.multiply_by_number(xi)
                    ptF = ptC.translated(vecCD)
            return Vector(ptE, ptF).length()
        else:
            det_alpha = b1*c22 - b2*c12
            det_gamma = c11*b2 + c12*b1
            alpha = det_alpha / det
            gamma = det_gamma / det
            vecAB.multiply_by_number(alpha)
            if 0 <= alpha <= 1:
                ptE = ptA.translated(vecAB)
            elif alpha < 0:
                ptE = ptA
            else:
                ptE = ptB
            vecCD.multiply_by_number(gamma)
            if 0 <= gamma <= 1:
                ptF = ptC.translated(vecCD)
            elif gamma < 0:
                ptF = ptC
            else:
                ptF = ptD
            return Vector(ptE, ptF).length()

    def __distance_segment_plane(self, segment, plane):
        # side is a parameter to characterize
        # whether segment crosses plane
        # (from what side of a plane the point is)
        side = plane.get_point_sign
        if side(segment.begin) != side(segment.end):
            return 0
        distance = self.__distance_point_plane
        return min(distance(segment.begin, plane),
                   distance(segment.end, plane))

    def __distance_segment_polygon(self, segment, polygon):
        distance = self.__distance_segment_segment
        edge = Segment(polygon.vertices[0], polygon.vertices[-1])
        min_edge_distance = distance(segment, edge)
        for i in range(1, len(polygon.vertices)):
            edge = Segment(polygon.vertices[i], polygon.vertices[i - 1])
            min_edge_distance = min(min_edge_distance,
                                    distance(segment, edge))
        pl = polygon.containing_plane
        if self.__distance_segment_plane(segment, pl) != 0:
            return min_edge_distance
        #ptCross = begin + alpha*Vector(segment)
        pt = segment.begin
        vec = Vector(segment)
        alpha = ((-pl.a*pt.x - pl.b*pt.y - pl.c*pt.z - pl.d) /
                 (vec.x + vec.y + vec.z))
        ptCross = Point(pt.x + alpha*vec.x,
                        pt.y + alpha*vec.y,
                        pt.z + alpha*vec.z)
        if self.__distance_point_polygon(ptCross, polygon) == 0:
            return 0
        return min_edge_distance

    def __distance_segment_prism(self, segment, prism):
        distance = self.__distance_segment_polygon
        result = min(distance(segment, prism.top_facet),
                     distance(segment, prism.bottom_facet))
        # side facets:
        for i in range(len(prism.top_facet.vertices)):
            if i == 0:
                j = len(prism.top_facet.vertices) - 1
            else:
                j = i - 1
            side_facet = PolygonRegular([prism.top_facet.vertices[i],
                                         prism.top_facet.vertices[j],
                                         prism.bottom_facet.vertices[j],
                                         prism.bottom_facet.vertices[i]])
            result = min(result, distance(segment, side_facet))
        return result

    def __distance_plane_point(self, plane, point):
        return self.__distance_point_plane(point, plane)

    def __distance_plane_line(self, plane, line):
        return self.__distance_line_plane(line, plane)

    def __distance_plane_segment(self, plane, segment):
        return self.__distance_segment_plane(segment, plane)

    def __distance_plane_plane(self, plane1, plane2):
        # normal1 =  (+-)normal2 otherwise they cross
        if (plane1.a != plane2.a or
            plane1.b != plane2.b or
            plane1.c != plane2.c) and (plane1.a != -plane2.a and
                                       plane1.b != -plane2.b and
                                       plane1.c != -plane2.c):
            return 0
        return abs(plane1.d - plane2.d)

    def __distance_plane_polygon(self, plane, polygon):
        distance = self.__distance_segment_plane
        edge = Segment(polygon.vertices[0], polygon.vertices[-1])
        result = distance(edge, plane) # start value
        for i in range(len(polygon.vertices)):
            result = min(result, distance(edge, plane))
        return result

    def __distance_plane_prism(self, plane, prism):
        distance = self.__distance_plane_polygon
        result = min(distance(plane, prism.top_facet),
                     distance(plane, prism.bottom_facet)) # start value
        for i in range(len(prism.top_facet.vertices)):
            side_facet = PolygonRegular([prism.top_facet.vertices[i],
                                         prism.top_facet.vertices[i - 1],
                                         prism.bottom_facet.vertices[i - 1],
                                         prism.bottom_facet.vertices[i]])
            result = min(result, distance(plane, side_facet))
        return result

    def __distance_polygon_point(self, polygon, point):
        return self.__distance_point_polygon(point, polygon)

    def __distance_polygon_line(self, polygon, line):
        return self.__distance_line_polygon(line, polygon)

    def __distance_polygon_segment(self, polygon, segment):
        return self.__distance_segment_polygon(segment, polygon)

    def __distance_polygon_plane(self, polygon, plane):
        return self.__distance_plane_polygon(plane, polygon)

    def __distance_polygon_polygon(self, polygon1, polygon2):
        # result = min_edge_edge_distance if one does not contain another
        distance = self.__distance_segment_polygon
        distances12 = [] # distnaces from edges of polygon1 to polygon2
        distances21 = [] # distances from edges of polygon2 to polygon1
        for i in range(len(polygon1.vertices)):
            edge1 = Segment(polygon1.vertices[i], polygon1.vertices[i - 1])
            distances12.append(distance(edge1, polygon2))
        for i in range(len(polygon2.vertices)):
            edge2 = Segment(polygon2.vertices[i], polygon2.vertices[i - 1])
            distances21.append(distance(edge2, polygon1))
        min_distance = min(min(distances12), min(distances12))
        ac = AffinityChecker()
        if ac.check(polygon1, polygon2) or ac.check(polygon2, polygon1):
            return 0
        return min_distance

    def __distance_polygon_prism(self, polygon, prism):
        # result = min_facet_polygon_distance
        # if prism does not contain polygon
        distance = self.__distance_polygon_polygon
        result = min(distance(polygon, prism.top_facet),
                     distance(polygon, prism.bottom_facet))
        for i in range(len(prism.top_facet.vertices)):
            side_facet = PolygonRegular([prism.top_facet.vertices[i],
                                         prism.top_facet.vertices[i - 1],
                                         prism.bottom_facet.vertices[i - 1],
                                         prism.bottom_facet.vertices[i]])
            result = min(result, distance(polygon, side_facet))
        ac = AffinityChecker()
        if ac.check(polygon, prism):
            return 0
        return result

    def __distance_prism_point(self, prism, point):
        return self.__distance_point_prism(point, prism)

    def __distance_prism_line(self, prism, line):
        return self.__distance_line_prism(line, prism)

    def __distance_prism_segment(self, prism, segment):
        return self.__distance_segment_prism(segment, prism)

    def __distance_prism_plane(self, prism, plane):
        return self.__distance_plane_prism(plane, prism)

    def __distance_prism_polygon(self, prism, polygon):
        return self.__distance_polygon_prism(polygon, prism)

    def __distance_prism_prism(self, prism1, prism2):
        # return minimal distance between facets
        # if one does not contain another
        ac = AffinityChecker()
        if ac.check(prism1, prism2) or ac.check(prism2, prism1):
            return 0
        prism1_facets = [prism1.top_facet, prism1.bottom_facet]
        for i in range(len(prism1.top_facet.vertices)):
            side_facet1 = PolygonRegular([prism1.top_facet.vertices[i],
                                          prism1.top_facet.vertices[i - 1],
                                          prism1.bottom_facet.vertices[i - 1],
                                          prism1.bottom_facet.vertices[i]])
            prism1_facets.append(side_facet1)
        prism2_facets = [prism2.top_facet, prism2.bottom_facet]
        for i in range(len(prism2.top_facet.vertices)):
            side_facet2 = PolygonRegular([prism2.top_facet.vertices[i],
                                          prism2.top_facet.vertices[i - 1],
                                          prism2.bottom_facet.vertices[i - 1],
                                          prism2.bottom_facet.vertices[i]])
            prism2_facets.append(side_facet2)
        distance = self.__distance_polygon_polygon
        min_distance = distance(prism1_facets[0], prism2_facets[0]) # start value
        for i, facet1 in enumerate(prism1_facets):
            for j, facet2 in enumerate(prism2_facets):
                min_distance = min(min_distance, distance(facet1, facet2))
        return min_distance
