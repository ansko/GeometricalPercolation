#include "../../include/geometries/polygon.hpp"

Polygon::Polygon(std::vector<Point> vertices) {
    __vertices = vertices;
};

std::vector<Point> Polygon::vertices() {
    return __vertices;
};

Point Polygon::center() {
    Vector center;
    for (auto vertex : __vertices)
        center = center + Vector(vertex.x(), vertex.y(), vertex.z());
    center = center / __vertices.size();
    return Point(center.x(), center.y(), center.z());
}

bool Polygon::crossesOtherPolygon(Polygon otherPolygon) {
    std::vector<Point> otherVertices = otherPolygon.vertices();
    Plane otherPlane = Plane(otherVertices[0], otherVertices[1], otherVertices[2]);
    Plane plane = Plane(__vertices[0], __vertices[1], __vertices[2]);
    bool flagSelfCrossesOther = false;
    bool flagOtherCrossesSelf = false;
    for (int i = 0; i < __vertices.size(); ++i) {
        Point ptBegin = __vertices[i];
        Point ptEnd;
        if (i != __vertices.size() - 1)
            ptEnd = __vertices[i + 1];
        else
            ptEnd = __vertices[0];
        LineSegment ls = LineSegment(ptBegin, ptEnd);
        if (otherPlane.isCrossedByLineSegment(ls)) {
            Point ptCross = otherPlane.ptCross();
            if (otherPolygon.containsPoint(ptCross)) {
                flagSelfCrossesOther = true;
                break;
            }
        }
    }
    if (flagSelfCrossesOther == true) {
            return true;
    }
    for (int i = 0; i < otherVertices.size(); ++i) {
        Point ptBegin = otherVertices[i];
        Point ptEnd;
        if (i != otherVertices.size() - 1)
            ptEnd = otherVertices[i + 1];
        else
            ptEnd = otherVertices[0];
        LineSegment ls = LineSegment(ptBegin, ptEnd);
        if (plane.isCrossedByLineSegment(ls)) {
            Point ptCross = plane.ptCross();
            if (this->containsPoint(ptCross)) {
                flagOtherCrossesSelf = true;
                break;
            }
        }
    }
    if (flagOtherCrossesSelf == true)
        return true;
    return false;
};

bool Polygon::containsPoint(Point pt) {
    float eps = 0.000001;
    int s = __vertices.size();
    int flag = 0;
    Vector center, otherCenter;
    for (auto vertex : __vertices)
        center = center + Vector(vertex.x(), vertex.y(), vertex.z());
    center = center / s;
    Point pt0, pt1, pt2;
    for(int i = 0; i < s; ++i) {
        if (i == s - 1) {
            pt0 = __vertices[i];
            pt1 = __vertices[0];
            pt2 = __vertices[1];
        }
        else if (i == s - 2) {
            pt0 = __vertices[i];
            pt1 = __vertices[i + 1];
            pt2 = __vertices[0];
        }
        else {
            pt0 = __vertices[i];
            pt1 = __vertices[i + 1];
            pt2 = __vertices[i + 2];
        }
        Plane pl = Plane(pt0, pt1, pt2);
        Vector v02 = Vector(pt0, pt2);
        Vector v01 = Vector(pt0, pt1);
        Vector v0pt = Vector(pt0, pt);
        float tmp = v02.vectorMultiply(v01).scalarMultiply(v01.vectorMultiply(v0pt));
        if (tmp > eps)
            flag = 1;
    }
    if (flag == 0)
        return true;
    return false;
}; 

bool Polygon::crossesBox(float boxSize) {
    for (int i = 0; i < __vertices.size(); ++i) {
        auto vertex = __vertices[i];
        if (vertex.x() < 0 || vertex.x() > boxSize)
            return true;
        if (vertex.y() < 0 || vertex.y() > boxSize)
            return true;
        if (vertex.z() < 0 || vertex.z() > boxSize)
            return true;
    }
    return false;
};
