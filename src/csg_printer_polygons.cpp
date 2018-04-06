#include "../include/csg_printer_polygons.hpp"


const float  PI_F = 3.14159265358979;


void CSGPrinterPolygons::printToCSGAsPolygonalCylindersShells(
         std::string fname,
         std::vector<std::shared_ptr<PolygonalCylinder> > polCyl_ptrs,
         std::vector<std::shared_ptr<PolygonalCylinder> > sh_ptrs
)
{
    std::ofstream fout;
    fout.open(fname);

    SettingsParser sp("/home/anton/Projects/CppPolygons_old/tmp/options.ini");
    sp.parseSettings();
    std::string CUBE_EDGE_LENGTH = sp.getProperty("CUBE_EDGE_LENGTH");
    std::string VERTICES_NUMBER = sp.getProperty("VERTICES_NUMBER");
    float verticesNumber = std::stof(VERTICES_NUMBER);
    std::string THICKNESS = sp.getProperty("THICKNESS");
    float sh = std::stof(sp.getProperty("SHELL_THICKNESS"));
    std::string OUTER_RADIUS = sp.getProperty("OUTER_RADIUS");
    float edgeLength = (float)std::stod(OUTER_RADIUS)
                           * 2 * sin(PI_F / verticesNumber);
    float innerRadius = edgeLength / 2 / tan(PI_F / verticesNumber);

    std::string fillerString = "solid filler = polygonalCylinder0";
    std::string shellsString = "solid shells = pc0";
    fout << "algebraic3d\n";
    fout << "solid cell = orthobrick(0, 0, 0; ";
    fout << CUBE_EDGE_LENGTH << ", "\
         << CUBE_EDGE_LENGTH << ", "\
         << CUBE_EDGE_LENGTH << ");\n";

    if (polCyl_ptrs.size() > 0) {
          // cores
        for (int i = 0; i < polCyl_ptrs.size(); ++i) {
            Point tfc = polCyl_ptrs[i]->getTfc();
            Point bfc = polCyl_ptrs[i]->getBfc();
            Point cc = Point(tfc.x() / 2 + bfc.x() / 2,
                             tfc.y() / 2 + bfc.y() / 2,
                             tfc.z() / 2 + bfc.z() / 2);
            Vector tb(tfc, bfc);

            fout << "solid polygonalCylinder" << i << " =\n plane("
                         << tfc.x() << ", " << tfc.y() << ", " << tfc.z() << "; "
                         << -tb.x() << ", "
                         << -tb.y() << ", "
                         << -tb.z() << ")" 
                         << "\n and plane("
                         << bfc.x() << ", " << bfc.y() << ", " << bfc.z() << "; "
                         << tb.x() << ", "
                         << tb.y() << ", "
                         << tb.z() << ")\n";
            for (uint j = 0; j < polCyl_ptrs[i]->facets().size(); ++j) {
                Polygon facet = polCyl_ptrs[i]->facets()[j];
                Vector cf = Vector(cc, facet.center());
                fout << " and plane("
                     << facet.center().x() << ", "
                     << facet.center().y() << ", "
                     << facet.center().z() << "; "
                     << cf.x() << ", "
                     << cf.y() << ", "
                     << cf.z() << ")";
                if (j == polCyl_ptrs[i]->facets().size() - 1)
                     fout << " and cell;";
                fout << "\n";
            }

            if (i != 0)
                fillerString += " or polygonalCylinder" + std::to_string(i);
        }
         // shells
        for (int i = 0; i < sh_ptrs.size(); ++i) {
            Point tfc = sh_ptrs[i]->getTfc();
            Point bfc = sh_ptrs[i]->getBfc();
            Point cc = Point(tfc.x() / 2 + bfc.x() / 2,
                             tfc.y() / 2 + bfc.y() / 2,
                             tfc.z() / 2 + bfc.z() / 2);
            Vector tb(tfc, bfc);

            fout << "solid pc" << i << " =\n plane("
                         << tfc.x() << ", " << tfc.y() << ", " << tfc.z() << "; "\
                         << -tb.x() << ", "
                         << -tb.y() << ", "
                         << -tb.z() << ")" \
                         << "\n and plane("
                         << bfc.x() << ", " << bfc.y() << ", " << bfc.z() << "; "\
                         << tb.x() << ", "
                         << tb.y() << ", "
                         << tb.z() << ")\n";
            for (uint j = 0; j < sh_ptrs[i]->facets().size(); ++j) {
                Polygon facet = sh_ptrs[i]->facets()[j];
                Vector cf = Vector(cc, facet.center());
                fout << "and plane("
                     << facet.center().x() << ", "
                     << facet.center().y() << ", "
                     << facet.center().z() << "; "
                     << cf.x() << ", "
                     << cf.y() << ", "
                     << cf.z() << ")";
                if (j == sh_ptrs[i]->facets().size() - 1)
                     fout << "and cell;";
                fout << "\n";
            }

            if (i != 0)
                shellsString += " or pc" + std::to_string(i);
        }
    }
    fout << fillerString << ";" << std::endl;
    fout << shellsString << ";" << std::endl;
    fout << "tlo filler;\n";
    fout << "solid interface = shells and not filler;\n";
    fout << "tlo interface -transparent;\n";
    fout << "solid matrix = not shells and cell;\n";
    fout << "tlo matrix -transparent;\n";    
    fout.close();
    return;
};
