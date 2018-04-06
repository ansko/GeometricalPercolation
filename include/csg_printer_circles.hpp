#include <fstream>
#include <memory>
#include <string>
#include <vector>

#include "geometries/plane.hpp"
#include "geometries/polygonal_cylinder.hpp"
#include "settings_parser.hpp"


const float  PI_F = 3.14159265358979f;


class CSGPrinterCircles
{
public:
    void printToCSGAsCircleCylindersShells(
         std::string fname,
         std::vector<std::shared_ptr<PolygonalCylinder> > polCyl_ptrs,
         std::vector<std::shared_ptr<PolygonalCylinder> > sh_ptrs
    );
};
