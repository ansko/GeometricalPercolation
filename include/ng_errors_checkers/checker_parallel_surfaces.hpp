#pragma once


#include <cmath>

#include <memory>
#include <vector>

#include "../geometries/plane.hpp"
#include "../geometries/polygon.hpp"
#include "../geometries/polygonal_cylinder.hpp"
#include "../geometries/vector.hpp"


class CheckerParallelSurfaces
{
public:
    CheckerParallelSurfaces(std::vector<std::shared_ptr<PolygonalCylinder> > cyl_ptrs);
    float check(); // returns the smalles angle between two surfaces;
                   // I suppose that some critical value of this angle exists
private:
    std::vector<std::shared_ptr<PolygonalCylinder> > cyl_ptrs;
};
