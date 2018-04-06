#pragma once

#include <cmath>
#include <iostream>
#include <vector>

#include "point.hpp"

class Vector {
public:
    Vector();
    Vector(Point begin, Point end);
    Vector(float x, float y, float z);

    Vector operator+(Vector otherVector);
    Vector operator-(Vector otherVector);
    Vector operator*(float coefficient);
    Vector operator/(float coefficient);

    float x();
    void setX(float newX);
    float y();
    void setY(float newY);
    float z();
    void setZ(float newZ);
    float length();

    Vector vectorMultiply(Vector otherVector);
    float scalarMultiply(Vector otherVector);
    Vector dot4(std::vector<std::vector<float> > M); // to translate or rotate by matrix
private:
    Point __begin, __end;
};
