#pragma once

#include <vector>

#include "line_segment.hpp"
#include "plane.hpp"
#include "point.hpp"


class Polygon {
public:
    Polygon(std::vector<Point> vertices);
    std::vector<Point> vertices();
    bool crossesOtherPolygon(Polygon otherPolygon);
    bool containsPoint(Point pt);        
    bool crossesBox(float boxSize);
    Point center();
private:
    std::vector<Point> __vertices;
};
