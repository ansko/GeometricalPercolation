#include <iostream>
#include <memory>
#include <vector>
#include <ctime>
#include <cstdlib>

#include "include/settings_parser.hpp"
#include "include/csg_printer_circles.hpp"
#include "include/csg_printer_polygons.hpp"
#include "include/geometries/polygonal_cylinder.hpp"
#include "include/ng_errors_checkers/checker_parallel_surfaces.hpp"
#include "include/percolation/percolation_checker.hpp"


int main(int argc, char **argv)
{
    // parsing settings
    SettingsParser sp("options.ini");
    sp.parseSettings();
    float cubeSize = (float)std::stod(sp.getProperty("CUBE_EDGE_LENGTH"));
    int n = (int)std::stod(sp.getProperty("VERTICES_NUMBER"));
    float h = (float)std::stod(sp.getProperty("THICKNESS"));
    float sh = (float)std::stod(sp.getProperty("SHELL_THICKNESS"));
    float R = (float)std::stod(sp.getProperty("OUTER_RADIUS"));
    int N = (int)std::stod(sp.getProperty("DISKS_NUM"));
    int MAX_ATTEMPTS = (int)std::stod(sp.getProperty("MAX_ATTEMPTS"));
    std::string FNAME = sp.getProperty("FNAME");
    std::string FNAME_LOG = sp.getProperty("FNAME_LOG");
    std::string PERC_FNAME = sp.getProperty("PERC_FNAME");
    float edgeLength = R * 2  * sin(PI_F / n);
    float innerRadius = edgeLength / 2 / tan(PI_F / n);
    float r = R * cos(PI_F / n);
    // starting to create initial configuration
    std::vector<std::shared_ptr<PolygonalCylinder> > polCyls;
    std::vector<std::shared_ptr<PolygonalCylinder> > shells;
    int attempt = 0;
    srand(time(NULL));
    while(polCyls.size() < N && ++attempt < MAX_ATTEMPTS) {
        std::shared_ptr<PolygonalCylinder> polCyl_ptr =
            std::make_shared<PolygonalCylinder>(n, h, R);
        std::shared_ptr<PolygonalCylinder> sh_ptr =
            std::make_shared<PolygonalCylinder>(n, h + 2 * sh, R + sh);
        float dx = static_cast<float>(rand()) / RAND_MAX * cubeSize;
        float dy = static_cast<float>(rand()) / RAND_MAX * cubeSize;
        float dz = static_cast<float>(rand()) / RAND_MAX * cubeSize;
        float alpha = static_cast<float>(rand()) / RAND_MAX;
        float beta = static_cast<float>(rand()) / RAND_MAX;
        float gamma = static_cast<float>(rand()) / RAND_MAX;
        polCyl_ptr->rotateAroundX(PI_F * alpha);
        polCyl_ptr->rotateAroundY(PI_F * beta);
        polCyl_ptr->rotateAroundZ(PI_F * gamma);
        polCyl_ptr->translate(dx, dy, dz);
        sh_ptr->rotateAroundX(PI_F * alpha);
        sh_ptr->rotateAroundY(PI_F * beta);
        sh_ptr->rotateAroundZ(PI_F * gamma);
        sh_ptr->translate(dx, dy, dz);
        if (polCyl_ptr->crossesBox(cubeSize))
            continue;
        int flag = 0;
        for(auto oldPc : polCyls)
            if (polCyl_ptr->crossesOtherPolygonalCylinder(*oldPc, 0)) {
                flag = 1;
                break;
            }
        if(flag == 1)
            continue;
        polCyls.push_back(polCyl_ptr);
        shells.push_back(sh_ptr);
    } 
    float pcVolume =  PI_F * pow(r, 2) * h;
    float shVolume =  PI_F * pow(r + sh, 2) * (h + 2 * sh);
    float cubeVolume = pow(cubeSize, 3);
    std::ofstream fout;
    fout.open(FNAME_LOG, std::ofstream::app);
    fout << "cpp: fi:                 "
         << polCyls.size() * pcVolume / cubeVolume
         << "\ncpp: CylsNum:            " << polCyls.size()
         << "\ncpp: Attempts:           " << attempt << std::endl;
    std::shared_ptr<CSGPrinterPolygons> printer_ptr;
    fout.close();
    printer_ptr->printToCSGAsPolygonalCylindersShells(FNAME, polCyls, shells);
    PercolationChecker pc(shells); 
    pc.sideToSide();
    return 0;
}
