#include "../../include/ng_errors_checkers/checker_parallel_surfaces.hpp"


const float  PI_F = 3.14159265358979;


CheckerParallelSurfaces::CheckerParallelSurfaces(
    std::vector<std::shared_ptr<PolygonalCylinder> > cyl_ptrs)
{
    this->cyl_ptrs = cyl_ptrs;
}

float CheckerParallelSurfaces::check()
{
    float max_cos_value = 0.0; // start value, all values are taken by their modulus
    float min_angle_value = acos(max_cos_value);

    std::vector<Vector> normals; // normals to every surface in the system
    for (auto& cyl_ptr : this->cyl_ptrs) {
        Point tfc, bfc, c;
        tfc = cyl_ptr->getTfc();
        bfc = cyl_ptr->getBfc();
        c = Point((tfc.x() + bfc.x()) / 2,
                  (tfc.y() + bfc.y()) / 2,
                  (tfc.z() + bfc.z()) / 2);
        std::vector<Polygon> facets = cyl_ptr->facets();
        for (auto& facet : facets)
            normals.push_back(Vector(c, facet.center()));
        normals.push_back(Vector(tfc, bfc));
    }

    for (uint i = 0; i < normals.size(); ++i)
        for (uint j = 0; j < normals.size(), j != i; ++j) {
            Vector ni = normals[i];
            Vector nj = normals[j];
            float li = pow(ni.x() * ni.x() + ni.y() * ni.y() + ni.z() * ni.z(), 0.5);
            float lj = pow(nj.x() * nj.x() + nj.y() * nj.y() + nj.z() * nj.z(), 0.5);
            if (li == 0 || lj == 0)
                std::cout << "ERROR: " << i << " " << j << std::endl;
            float cos_value = (ni.x() * nj.x() + ni.y() * nj.y() + ni.z() * nj.z()) / li / lj;
            //if (cos_value < 0)
            //    cos_value = (-1.0) * cos_value;
            //std::cout << "tmp cos value: " << cos_value << std::endl;
            if (cos_value > max_cos_value)
                max_cos_value = cos_value;
        }
    std::cout << "Max cos: " << max_cos_value + 0.00000001 << std::endl;
    std::cout << "Min angle: " << acos(max_cos_value) << std::endl;
    min_angle_value = acos(max_cos_value);
    return min_angle_value;
}
