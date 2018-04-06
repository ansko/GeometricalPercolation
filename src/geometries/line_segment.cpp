#include <cmath>

#include "../../include/geometries/line_segment.hpp"


LineSegment::LineSegment(Point ptBegin, Point ptEnd) {
    __begin = ptBegin;
    __end = ptEnd;
};

float LineSegment::x() {
    return __begin.x() - __end.x();
};

float LineSegment::y() {
    return __begin.y() - __end.y();
};

float LineSegment::z() {
    return __begin.z() - __end.z();
};

float LineSegment::length() {
    return pow(pow(this->x(), 2) + pow(this->y(), 2) + pow(this->z(), 2), 0.5);
};

Point LineSegment::begin() {
    return __begin;
};

Point LineSegment::end() {
    return __end;
};

bool LineSegment::isCrossedByOtherLineSegment(LineSegment otherLs) {
    // TODO
    return true;
};
