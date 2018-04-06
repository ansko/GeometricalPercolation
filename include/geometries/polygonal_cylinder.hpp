#pragma once

#include <memory>
#include <string>
#include <vector>

#include "point.hpp"
#include "polygon.hpp"


class PolygonalCylinder {
public:
    PolygonalCylinder(int verticesNumber, float thickness, float outerRadius);
    PolygonalCylinder(std::shared_ptr<Polygon> top_facet_ptr,
                      std::shared_ptr<Polygon> bottom_facet_ptr);
    Polygon topFacet();
    Polygon bottomFacet();
    std::vector<Polygon> facets();
    bool crossesOtherPolygonalCylinder(
        PolygonalCylinder otherPolygonalCylinder, int mode
    );
    virtual bool crossesBox(float boxSize);
    void translate(float dx, float dy, float dz);
    void rotateAroundX(float angle);
    void rotateAroundY(float angle);
    void rotateAroundZ(float angle);
    Point getTfc();
    Point getBfc();
    float getR();
protected:
    std::vector<Polygon> __facets;
    std::shared_ptr<Polygon> topFacet_ptr, bottomFacet_ptr;
    int __verticesNumber;
    float __thickness;
    float __outerRadius;
    Point tfc;
    Point bfc;
};
