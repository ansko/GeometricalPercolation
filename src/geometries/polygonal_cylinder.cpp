#include <cmath>
#include <iostream>

#include "../../include/geometries/polygonal_cylinder.hpp"

const float  PI_F = 3.14159265358979f;


PolygonalCylinder::PolygonalCylinder(
    int verticesNumber,
    float thickness,
    float outerRadius
    ) {
    __outerRadius = outerRadius;
    __verticesNumber = verticesNumber;
    __thickness = thickness;
    __outerRadius = outerRadius;
    float centralAngle = 2 * PI_F / verticesNumber;
    std::vector<Point> centralVertices, topVertices, bottomVertices;
    for(int i = 0; i < verticesNumber; i++) {
        centralVertices.clear();
        topVertices.push_back(Point(outerRadius * cos(centralAngle * i),
                                    outerRadius * sin(centralAngle * i),
                                    thickness / 2));
        bottomVertices.push_back(Point(outerRadius * cos(centralAngle * i),
                                       outerRadius * sin(centralAngle * i),
                                       -thickness / 2));
        // central vertices == vertices of side facets
        // (2 from top, 2 from bottom)
        centralVertices.push_back(Point(outerRadius * cos(centralAngle * (i - 1)),
                                        outerRadius * sin(centralAngle * (i - 1)),
                                        thickness / 2));
        centralVertices.push_back(Point(outerRadius * cos(centralAngle * i),
                                        outerRadius * sin(centralAngle * i),
                                        thickness / 2));
        centralVertices.push_back(Point(outerRadius * cos(centralAngle * i),
                                        outerRadius * sin(centralAngle * i),
                                        -thickness / 2));
        centralVertices.push_back(Point(outerRadius * cos(centralAngle * (i - 1)),
                                        outerRadius * sin(centralAngle * (i - 1)),
                                        -thickness / 2));
        __facets.push_back(Polygon(centralVertices));
    }
    topFacet_ptr = std::make_shared<Polygon>(Polygon(topVertices));
    bottomFacet_ptr = std::make_shared<Polygon>(Polygon(bottomVertices));
    tfc = Point(0, 0, thickness / 2);
    bfc = Point(0, 0, -thickness / 2);
};


PolygonalCylinder::PolygonalCylinder(
        std::shared_ptr<Polygon> top_facet_ptr,
        std::shared_ptr<Polygon> bottom_facet_ptr) {
    std::shared_ptr<std::vector<Point> > top_vertices_ptr =
        std::make_shared<std::vector<Point> >(top_facet_ptr->vertices());
    std::shared_ptr<std::vector<Point> > bottom_vertices_ptr =
        std::make_shared<std::vector<Point> >(bottom_facet_ptr->vertices());
    uint vertices_number = top_facet_ptr->vertices().size();
    for (uint vertex_number = 0; vertex_number < vertices_number; ++ vertex_number) {
        std::vector<Point> side_vertices;
        uint other_vertex_number = vertex_number - 1;
        if (vertex_number == 0)
            other_vertex_number = vertices_number - 1;
        side_vertices.push_back(top_facet_ptr->vertices()[vertex_number]);
        side_vertices.push_back(top_facet_ptr->vertices()[other_vertex_number]);
        side_vertices.push_back(bottom_facet_ptr->vertices()[other_vertex_number]);
        side_vertices.push_back(bottom_facet_ptr->vertices()[vertex_number]);
        __facets.push_back(Polygon(side_vertices));

    }
    {
        Point pt1 = top_facet_ptr->vertices()[0],
              pt2 = top_facet_ptr->vertices()[1],
              pt3 = bottom_facet_ptr->vertices()[0];
        float edge_length = Vector(pt1, pt2).length();
        __outerRadius = edge_length / 2 / sin(PI_F / vertices_number);
        __verticesNumber = vertices_number;
        __thickness = Vector(pt1, pt3).length();
    }
{
    float tfc_x = 0, tfc_y = 0, tfc_z = 0,
          bfc_x = 0, bfc_y = 0, bfc_z = 0;
    for (uint vertex_number = 0; vertex_number < vertices_number; ++ vertex_number) {
        tfc_x += top_facet_ptr->vertices()[vertex_number].x();
        tfc_y += top_facet_ptr->vertices()[vertex_number].y();
        tfc_z += top_facet_ptr->vertices()[vertex_number].z();
        bfc_x += bottom_facet_ptr->vertices()[vertex_number].x();
        bfc_y += bottom_facet_ptr->vertices()[vertex_number].y();
        bfc_z += bottom_facet_ptr->vertices()[vertex_number].z();
    }
    tfc = Point(tfc_x / vertices_number, tfc_y / vertices_number, tfc_z / vertices_number);
    bfc = Point(bfc_x / vertices_number, bfc_y / vertices_number, bfc_z / vertices_number);
}
    topFacet_ptr = top_facet_ptr;
    bottomFacet_ptr = bottom_facet_ptr;
}


Point PolygonalCylinder::getTfc() {
    return this->tfc;
}

Point PolygonalCylinder::getBfc() {
    return this->bfc;
}


std::vector<Polygon> PolygonalCylinder::facets() {
    return __facets;
};

Polygon PolygonalCylinder::topFacet() {
    return *topFacet_ptr;
};

Polygon PolygonalCylinder::bottomFacet() {
    return *bottomFacet_ptr;
};

float PolygonalCylinder::getR() {
    return __outerRadius;
}

bool PolygonalCylinder::crossesOtherPolygonalCylinder(
        PolygonalCylinder otherPolygonalCylinder,
        int mode) {
    float THICKNESS = __thickness;
    float OUTER_RADIUS = __outerRadius;
    float verticesNumber = __verticesNumber;
    float edgeLength = OUTER_RADIUS * 2  * sin(PI_F / verticesNumber);
    float innerRadius = edgeLength / 2 / tan(PI_F / verticesNumber);
    Point tc = topFacet_ptr->center();
    Point bc = bottomFacet_ptr->center();
    Point otherTc = otherPolygonalCylinder.topFacet().center();
    Point otherBc = otherPolygonalCylinder.bottomFacet().center();
    Vector vc = Vector(tc.x() + bc.x(), tc.y() + bc.y(), tc.z() + bc.z()) / 2;
    Point c(vc.x(), vc.y(), vc.z());
    Vector otherVc = Vector(otherTc.x() + otherBc.x(),
                            otherTc.y() + otherBc.y(),
                            otherTc.z() + otherBc.z()) / 2;
    Point otherC(otherVc.x(), otherVc.y(), otherVc.z());
    float centersDistance = Vector(c, otherC).length();
    float veryCloseDistance = std::min(THICKNESS, 2 * innerRadius);
    float veryFarDistance = 2 * pow(pow(innerRadius, 2) 
                                  + pow(THICKNESS/2, 2), 0.5);
    if (centersDistance > veryFarDistance)
        return false;
    else if (centersDistance < veryCloseDistance)
        return true;
//    std::cout << "    starting precise checking\n";
    // if main axes of the cylinders lie on far lines
    // http://en.wikipedia.org/wiki/Skew_lines#Distance_between_two_skew_lines
    // x = x1 + td1 and x = x2 + td2
    // d = |(d1 x d2) / |d1 x d2| * (x1 - x2)|
    Point x1 = bottomFacet_ptr->center();
    Vector d1(bottomFacet_ptr->center(), topFacet_ptr->center());
    Point x2 = otherPolygonalCylinder.bottomFacet().center();
    Vector d2(otherPolygonalCylinder.bottomFacet().center(),\
              otherPolygonalCylinder.topFacet().center());
    Vector n = d1.vectorMultiply(d2) / d1.vectorMultiply(d2).length();
    Vector dx(x1, x2);
    float d = fabs(n.scalarMultiply(dx));
    if (d > 2 * OUTER_RADIUS)
        return false;
    std::vector<Polygon> polys, otherPolys;
    polys.push_back(*topFacet_ptr);
    polys.push_back(*bottomFacet_ptr);
    for (auto& facet : __facets)
        polys.push_back(facet);
    otherPolys.push_back(otherPolygonalCylinder.topFacet());
    otherPolys.push_back(otherPolygonalCylinder.bottomFacet());
    for (auto& facet : otherPolygonalCylinder.facets())
        otherPolys.push_back(facet);
    Point pcitsc(tc.x() / 2 + bc.x() / 2,
                 tc.y() / 2 + bc.y() / 2,
                 tc.z() / 2 + bc.z() / 2);
    Vector vpcitsc = Vector(pcitsc.x(), pcitsc.y(), pcitsc.z());
    Point otherPcitsc(otherTc.x() / 2 + otherBc.x() / 2,
                      otherTc.y() / 2 + otherBc.y() / 2,
                      otherTc.z() / 2 + otherBc.z() / 2);
    Vector votherPcitsc = Vector(otherPcitsc.x(),
                                 otherPcitsc.y(),
                                 otherPcitsc.z());
    uint polys_size = polys.size();
    for (uint pi = 0; pi < polys_size; ++pi) {
        auto poly = polys[pi];
        Point polyc = poly.center();
        Vector vpcitscpolyc = Vector(pcitsc, polyc);
        float coeff = 1;
        std::vector<Point> pts;
        for (auto& vertex : poly.vertices()) {
            Vector vpcitscvertex = Vector(pcitsc, vertex);
            Vector vvertex = vpcitsc + vpcitscvertex * coeff;
            vertex = Point(vvertex.x(), vvertex.y(), vvertex.z());
            pts.push_back(vertex);
        }
        poly = Polygon(pts);
        uint otherPolys_size = otherPolys.size();
        for (uint opi = 0; opi < otherPolys_size; ++opi) {
            auto otherPoly = otherPolys[opi];
            Point otherPolyc = otherPoly.center();
            Vector othervpcitscpolyc = Vector(otherPcitsc, otherPolyc);
            float otherCoeff = 1.0;
            std::vector<Point> otherPts;
            for (auto& vertex : otherPoly.vertices()) {
                Vector vpcitscvertex = Vector(otherPcitsc, vertex);
                vpcitscvertex = vpcitscvertex * otherCoeff;
                Vector vvertex = votherPcitsc + vpcitscvertex;
                vertex = Point(vvertex.x(), vvertex.y(), vvertex.z());
                otherPts.push_back(vertex);
            }
            otherPoly = Polygon(otherPts);
            if (poly.crossesOtherPolygon(otherPoly))
                return true;
        }
    }
    return false;
}

bool PolygonalCylinder::crossesBox(float boxSize) {
    std::vector<Polygon> polygons;
    polygons.push_back(*topFacet_ptr);
    polygons.push_back(*bottomFacet_ptr);
    if (topFacet_ptr->center().x() <= 0 || topFacet_ptr->center().x() >= boxSize ||
        topFacet_ptr->center().y() <= 0 || topFacet_ptr->center().y() >= boxSize ||
        topFacet_ptr->center().z() <= 0 || topFacet_ptr->center().z() >= boxSize)
            return true;
    for(int i = 0; i < 2; i++)
        if (polygons[i].crossesBox(boxSize))
            return true;
    return false;
};

void PolygonalCylinder::translate(float dx, float dy, float dz) {
    std::vector<std::vector<float> > M;
    std::vector<float> s;
    M.push_back(s);
    M.push_back(s);
    M.push_back(s);
    M.push_back(s);
    M[0].push_back(1);
    M[0].push_back(0);
    M[0].push_back(0);
    M[0].push_back(0);
    M[1].push_back(0);
    M[1].push_back(1);
    M[1].push_back(0);
    M[1].push_back(0);
    M[2].push_back(0);
    M[2].push_back(0);
    M[2].push_back(1);
    M[2].push_back(0);
    M[3].push_back(dx);
    M[3].push_back(dy);
    M[3].push_back(dz);
    M[3].push_back(1);
    std::vector<Polygon> polygons;
    polygons.push_back(*topFacet_ptr);
    polygons.push_back(*bottomFacet_ptr);
    for (auto& facet : __facets)
        polygons.push_back(facet);

    for (int i = 0; i < polygons.size(); ++i) {
        std::vector<Point> pts;
        for (auto& vertex : polygons[i].vertices()) {
            Vector v(vertex.x(), vertex.y(), vertex.z());
            v = v.dot4(M);
            pts.push_back(Point(v.x(), v.y(), v.z()));
        }
        polygons[i] = Polygon(pts);
    }
    topFacet_ptr = std::make_shared<Polygon>(polygons[0]);
    bottomFacet_ptr = std::make_shared<Polygon>(polygons[1]);
    __facets.clear();
    for (int i = 2; i < polygons.size(); ++i)
        __facets.push_back(polygons[i]);

            Vector v(tfc.x(), tfc.y(), tfc.z());
            v = v.dot4(M);
            tfc = Point(v.x(), v.y(), v.z());
            v = Vector(bfc.x(), bfc.y(), bfc.z());
            v = v.dot4(M);
            bfc = Point(v.x(), v.y(), v.z());
};

void PolygonalCylinder::rotateAroundX(float angle) {
    std::vector<std::vector<float> > M;
    std::vector<float> s;
    M.push_back(s);
    M.push_back(s);
    M.push_back(s);
    M.push_back(s);
    M[0].push_back(1);
    M[0].push_back(0);
    M[0].push_back(0);
    M[0].push_back(0);
    M[1].push_back(0);
    M[1].push_back(cos(angle));
    M[1].push_back(-sin(angle));
    M[1].push_back(0);
    M[2].push_back(0);
    M[2].push_back(sin(angle));
    M[2].push_back(cos(angle));
    M[2].push_back(0);
    M[3].push_back(0);
    M[3].push_back(0);
    M[3].push_back(0);
    M[3].push_back(1);
    std::vector<Polygon> polygons;
    polygons.push_back(*topFacet_ptr);
    polygons.push_back(*bottomFacet_ptr);
    for (auto facet : __facets)
        polygons.push_back(facet);

    for (int i = 0; i < polygons.size(); ++i) {
        std::vector<Point> pts;
        for (auto vertex : polygons[i].vertices()) {
            Vector v(vertex.x(), vertex.y(), vertex.z());
            v = v.dot4(M);
            pts.push_back(Point(v.x(), v.y(), v.z()));
        }
        polygons[i] = Polygon(pts);
    }
    topFacet_ptr = std::make_shared<Polygon>(polygons[0]);
    bottomFacet_ptr = std::make_shared<Polygon>(polygons[1]);
    __facets.clear();
    for (int i = 2; i < polygons.size(); ++i)
        __facets.push_back(polygons[i]);

            Vector v(tfc.x(), tfc.y(), tfc.z());
            v = v.dot4(M);
            tfc = Point(v.x(), v.y(), v.z());
            v = Vector(bfc.x(), bfc.y(), bfc.z());
            v = v.dot4(M);
            bfc = Point(v.x(), v.y(), v.z());
};

void PolygonalCylinder::rotateAroundY(float angle) {
    std::vector<std::vector<float> > M;
    std::vector<float> s;
    M.push_back(s);
    M.push_back(s);
    M.push_back(s);
    M.push_back(s);
    M[0].push_back(cos(angle));
    M[0].push_back(0);
    M[0].push_back(sin(angle));
    M[0].push_back(0);
    M[1].push_back(0);
    M[1].push_back(1);
    M[1].push_back(0);
    M[1].push_back(0);
    M[2].push_back(-sin(angle));
    M[2].push_back(0);
    M[2].push_back(cos(angle));
    M[2].push_back(0);
    M[3].push_back(0);
    M[3].push_back(0);
    M[3].push_back(0);
    M[3].push_back(1);
    std::vector<Polygon> polygons;
    polygons.push_back(*topFacet_ptr);
    polygons.push_back(*bottomFacet_ptr);
    for (auto facet : __facets)
        polygons.push_back(facet);

    for (int i = 0; i < polygons.size(); ++i) {
        std::vector<Point> pts;
        for (auto vertex : polygons[i].vertices()) {
            Vector v(vertex.x(), vertex.y(), vertex.z());
            v = v.dot4(M);
            pts.push_back(Point(v.x(), v.y(), v.z()));
        }
        polygons[i] = Polygon(pts);
    }
    topFacet_ptr = std::make_shared<Polygon>(polygons[0]);
    bottomFacet_ptr = std::make_shared<Polygon>(polygons[1]);
    __facets.clear();
    for (int i = 2; i < polygons.size(); ++i)
        __facets.push_back(polygons[i]);

            Vector v(tfc.x(), tfc.y(), tfc.z());
            v = v.dot4(M);
            tfc = Point(v.x(), v.y(), v.z());
            v = Vector(bfc.x(), bfc.y(), bfc.z());
            v = v.dot4(M);
            bfc = Point(v.x(), v.y(), v.z());
};

void PolygonalCylinder::rotateAroundZ(float angle) {
    std::vector<std::vector<float> > M;
    std::vector<float> s;
    M.push_back(s);
    M.push_back(s);
    M.push_back(s);
    M.push_back(s);
    M[0].push_back(cos(angle));
    M[0].push_back(-sin(angle));
    M[0].push_back(0);
    M[0].push_back(0);
    M[1].push_back(sin(angle));
    M[1].push_back(cos(angle));
    M[1].push_back(0);
    M[1].push_back(0);
    M[2].push_back(0);
    M[2].push_back(0);
    M[2].push_back(1);
    M[2].push_back(0);
    M[3].push_back(0);
    M[3].push_back(0);
    M[3].push_back(0);
    M[3].push_back(1);
    std::vector<Polygon> polygons;
    polygons.push_back(*topFacet_ptr);
    polygons.push_back(*bottomFacet_ptr);
    for (auto facet : __facets)
        polygons.push_back(facet);

    for (int i = 0; i < polygons.size(); ++i) {
        std::vector<Point> pts;
        for (auto vertex : polygons[i].vertices()) {
            Vector v(vertex.x(), vertex.y(), vertex.z());
            v = v.dot4(M);
            pts.push_back(Point(v.x(), v.y(), v.z()));
        }
        polygons[i] = Polygon(pts);
    }
    topFacet_ptr = std::make_shared<Polygon>(polygons[0]);
    bottomFacet_ptr = std::make_shared<Polygon>(polygons[1]);
    __facets.clear();
    for (int i = 2; i < polygons.size(); ++i)
        __facets.push_back(polygons[i]);

            Vector v(tfc.x(), tfc.y(), tfc.z());
            v = v.dot4(M);
            tfc = Point(v.x(), v.y(), v.z());
            v = Vector(bfc.x(), bfc.y(), bfc.z());
            v = v.dot4(M);
            bfc = Point(v.x(), v.y(), v.z());
};
