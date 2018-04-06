#pragma once

#include "point.hpp"

class LineSegment {
public:
    LineSegment(Point ptBegin, Point ptEnd);

    float x();
    float y();
    float z();
    float length();
    Point begin();
    Point end();
    bool isCrossedByOtherLineSegment(LineSegment otherLs);
private:
    Point __begin, __end;
};
