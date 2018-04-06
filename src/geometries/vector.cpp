#include "../../include/geometries/vector.hpp"


Vector::Vector() {
    __begin = Point();
    __end = Point();
};

Vector::Vector(Point begin, Point end) {
    __begin = Point();
    __end = Point(end.x() - begin.x(), end.y() - begin.y(), end.z() - begin.z());
}

Vector::Vector(float x, float y, float z) {
    __begin = Point();
    __end = Point(x, y, z);
}


Vector Vector::operator+(Vector otherVector) {
    float x = this->x() + otherVector.x();
    float y = this->y() + otherVector.y();
    float z = this->z() + otherVector.z();
    return Vector(x, y, z);
}

Vector Vector::operator-(Vector otherVector) {
    float x = this->x() - otherVector.x();
    float y = this->y() - otherVector.y();
    float z = this->z() - otherVector.z();
    return Vector(x, y, z);
}

Vector Vector::operator*(float coefficient) {
    float x = this->x() * coefficient;
    float y = this->y() * coefficient;
    float z = this->z() * coefficient;
    return Vector(x, y, z);
}

Vector Vector::operator/(float coefficient) {
    float x = this->x() / coefficient;
    float y = this->y() / coefficient;
    float z = this->z() / coefficient;
    return Vector(x, y, z);
}


float Vector::x() {
    return __end.x();
}

void Vector::setX(float newX) {
    __end.setX(newX);
}

float Vector::y() {
    return __end.y();
}

void Vector::setY(float newY) {
    __end.setY(newY);
}

float Vector::z() {
    return __end.z();
}

void Vector::setZ(float newZ) {
    __end.setZ(newZ);
}

float Vector::length() {
    return sqrt(pow(__end.x(), 2) + pow(__end.y(), 2) + pow(__end.z(), 2));
}


Vector Vector::vectorMultiply(Vector otherVector) {
    float x = this->y() * otherVector.z() - this->z() * otherVector.y();
    float y = this->z() * otherVector.x() - this->x() * otherVector.z();
    float z = this->x() * otherVector.y() - this->y() * otherVector.x();
    return Vector(x, y, z);
}

float Vector::scalarMultiply(Vector otherVector) {
    return this->x() * otherVector.x() + \
           this->y() * otherVector.y() + \
           this->z() * otherVector.z();
}

Vector Vector::dot4(std::vector<std::vector<float> > M) {
    float x = this->x() * M[0][0] +\
              this->y() * M[1][0] +\
              this->z() * M[2][0] + M[3][0];
    float y = this->x() * M[0][1] +\
              this->y() * M[1][1] +\
              this->z() * M[2][1] + M[3][1];
    float z = this->x() * M[0][2] +\
              this->y() * M[1][2] +\
              this->z() * M[2][2] + M[3][2];
    return Vector(x, y, z);
};
