#include <fstream>
#include <memory>
#include <string>
#include <vector>

#include "geometries/plane.hpp"
#include "geometries/polygonal_cylinder.hpp"
#include "settings_parser.hpp"


class CSGPrinterPolygons
{
public:
    void printToCSGAsPolygonalCylindersShells(
         std::string fname,
         std::vector<std::shared_ptr<PolygonalCylinder> > polCyl_ptrs,
         std::vector<std::shared_ptr<PolygonalCylinder> > sh_ptrs
    );
};
