#include "../../include/geometries/point.hpp"


Point::Point() {
    __x = 0;
    __y = 0;
    __z = 0;
}

Point::Point(float x, float y, float z) {
    __x = x;
    __y = y;
    __z = z;
}


float Point::x() {
    return __x;
}

void Point::setX(float newX) {
    __x = newX;
}

float Point::y() {
    return __y;
}

void Point::setY(float newY) {
    __y = newY;
}

float Point::z() {
    return __z;
}

void Point::setZ(float newZ) {
    __z = newZ;
}
