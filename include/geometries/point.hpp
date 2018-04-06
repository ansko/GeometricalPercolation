#pragma once

class Point {
public:
    Point();
    Point(float x, float y, float z);

    float x();
    void setX(float newX);
    float y();
    void setY(float newY);
    float z();
    void setZ(float newZ);
private:
    float __x, __y, __z;
};
