from mypymath.geometry.figures.polygon_regular import PolygonRegular


class PrismRegular:
    """
    Prism with a regular polygon as base.
    top_facet is parallel to bottom_facet and
    height is perpendicular to both of them.
    """
    def __init__(self,
                 param1, param2): # (top_facet, bottom_facet)
        self.name = 'prism_regular'
        if (isinstance(param1, PolygonRegular) and
              isinstance(param2, PolygonRegular)):
            top_facet = param1
            bottom_facet = param2
            self.__init_primitive(top_facet, bottom_facet)
            return
        else:
            print('Error in RegularPrism.__init__:',
                  'incorrect argumetns')
            return None

    def __init_primitive(self, top_facet, bottom_facet):
        self.top_facet = top_facet
        self.bottom_facet = bottom_facet
        dx = top_facet.center.x - bottom_facet.center.x
        dy = top_facet.center.y - bottom_facet.center.y
        dz = top_facet.center.z - bottom_facet.center.z
        self.height = (dx**2 + dy**2 + dz**2)**0.5

    def __str__(self):
        result = 'prism_reg{\n  top['
        for vertex in self.top_facet.vertices:
            result += '\n    ' + str(vertex)
        result += ']\n  bot:'
        for vertex in self.bottom_facet.vertices:
            result += '\n    ' + str(vertex)
        result += ']\n}'
        return result
