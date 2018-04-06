#pragma once

#include <array>

#include "line_segment.hpp"
#include "point.hpp"
#include "vector.hpp"


#include "../det.hpp"


class Plane {
public:
    Plane(float a, float b, float c, float d);
    Plane(Vector n, Point pt);
    Plane(Point pt0, Point pt1, Point pt2);

    float a();
    float b();
    float c();
    float d();
    Vector n();
    Point pt0();
    Point pt1();
    Point pt2();
    Point ptCross();

    bool isCrossedByLineSegment(LineSegment ls);
private:
    float __a, __b, __c, __d;
    Vector __n;
    Point __pt0, __pt1, __pt2, __ptCross;
};
