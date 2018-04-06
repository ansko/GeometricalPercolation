#pragma once


#include <fstream>
#include <memory>
#include <vector>

#include "../settings_parser.hpp"
#include "../geometries/polygon.hpp"
#include "../geometries/polygonal_cylinder.hpp"


class PercolationChecker
{
public:
    PercolationChecker(
        std::vector<std::shared_ptr<PolygonalCylinder> > shell_ptrs);
    bool sideToSide();
private:
    std::vector<std::shared_ptr<PolygonalCylinder> > shell_ptrs;
};
