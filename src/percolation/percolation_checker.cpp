#include "../../include/percolation/percolation_checker.hpp"


PercolationChecker::PercolationChecker(
    std::vector<std::shared_ptr<PolygonalCylinder> > shell_ptrs)
{
    this->shell_ptrs = shell_ptrs;
}


bool PercolationChecker::sideToSide()
{
// Not a percolationChecker but IntersectionsCalculator
    // Finding intersections
    SettingsParser sp("options.ini");
    sp.parseSettings();
    std::string fname_intersections = sp.getProperty("FNAME_INTERSECTIONS");
    std::string fname_minmaxes = sp.getProperty("FNAME_MINMAXES");
    std::ofstream fout;
    fout.open(fname_intersections);
    std::vector<std::pair<int, int> > allIntersections;
    std::vector<std::vector<int> > chains;
    for(uint i = 0; i < shell_ptrs.size(); ++i)
        for(uint j = 0; j < shell_ptrs.size(); ++j) {
            if(i == j)
                continue;
            std::shared_ptr<PolygonalCylinder> pc_ptr = shell_ptrs[i];
            std::shared_ptr<PolygonalCylinder> pc1_ptr = shell_ptrs[j];
            if(pc_ptr->crossesOtherPolygonalCylinder(*pc1_ptr, 0)) {
                fout << i << " " << j << std::endl;
                allIntersections.push_back(std::pair<int, int>(i, j));
            }
        }
    float cubeSize = (float)std::stod(sp.getProperty("CUBE_EDGE_LENGTH"));
    fout.close();
    // Listing minmaxes for every particle in the system
    fout.open(fname_minmaxes);
    for(uint i = 0; i < shell_ptrs.size(); ++i) {
        auto shell_ptr = shell_ptrs[i];
        float minx = cubeSize;
        float maxx = 0;
        float miny = cubeSize;
        float maxy = 0;
        float minz = cubeSize;
        float maxz = 0;
        for (auto poly : shell_ptr->facets())
            for (auto vertex : poly.vertices()) {
                if (vertex.x() < minx)
                    minx = vertex.x();
                else if (vertex.x() > maxx)
                    maxx = vertex.x();
                if (vertex.y() < miny)
                    miny = vertex.y();
                else if (vertex.y() > maxy)
                    maxy = vertex.y();
                if (vertex.z() < minz)
                    minz = vertex.z();
                else if (vertex.z() > maxz)
                    maxz = vertex.z();
            }
        fout << minx << " " << maxx << " "
             << miny << " " << maxy << " "
             << minz << " " << maxz << std::endl;
    }
    fout.close();
}
