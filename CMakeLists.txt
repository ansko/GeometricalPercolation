cmake_minimum_required (VERSION 2.6) 
 
set (PROJECT cpppolygons) 
 
project (${PROJECT}) 

if (CMAKE_COMPILER_IS_GNUCXX)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Werror")
endif (CMAKE_COMPILER_IS_GNUCXX)

set (HEADERS 
    include/csg_printer_circles.hpp
    include/csg_printer_polygons.hpp
    include/det.hpp
    include/geometries/line_segment.hpp
    include/geometries/plane.hpp
    include/geometries/point.hpp
    include/geometries/polygon.hpp
    include/geometries/polygonal_cylinder.hpp
    include/geometries/vector.hpp
    include/ng_errors_checkers/checker_parallel_surfaces.hpp
    include/settings_parser.hpp
    include/percolation/percolation_checker.hpp)

set (SOURCES
    src/csg_printer_circles.cpp
    src/csg_printer_polygons.cpp
    src/det.cpp 
    src/geometries/line_segment.cpp
    src/geometries/plane.cpp
    src/geometries/point.cpp
    src/geometries/polygon.cpp
    src/geometries/polygonal_cylinder.cpp
    src/geometries/vector.cpp
    src/ng_errors_checkers/checker_parallel_surfaces.cpp
    src/settings_parser.cpp
    src/percolation/percolation_checker.cpp
   # just one of these!
    exfoliated_interface_percolation_polygons.cpp)
   # test.cpp)
   # test2.cpp)
   # reparsed_crosses.cpp)
   # reparsed_minmax.cpp)
   # test3.cpp)
   # src/mains/main_exfoliated.cpp
   # src/mains/main_exfoliated_interface.cpp)
   # src/mains/main_exfoliated_shell.cpp)
   # exfoliated_interface_percolation.cpp
   # mesher.cpp)
 
add_executable (${PROJECT} ${HEADERS} ${SOURCES})

set_target_properties(${PROJECT} PROPERTIES COMPILE_FLAGS "-std=c++14 -g -lm")
