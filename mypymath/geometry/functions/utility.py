from mypymath.linalg import Vector

from mypymath.geometry.figures import Point


class Utility:
    """
    A class to perform some easy  but common calculations.
    """
    def triangle_area(self, point1, point2, point3):
        vec12 = Vector(point1, point2)
        vec13 = Vector(point1, point3)
        length12 = vec12.length()
        length13 = vec13.length()
        if 0 in (length12, length13):
            return 0
        cos_angle213 = vec12.product_with(vec13) / length12 / length13
        sin_angle213 = (1 - cos_angle213**2)**0.5
        area = 0.5 * sin_angle213 * length12 * length13
        return area
