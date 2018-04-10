# GeometricalPercolation
It must be the final repo for FEM, but more looks like just one of first drafts.

# This produces cpppolygons executable

cmake CMakeLists
make

running ./cpppolygons one can get a ternary system of polygonal cylinders:
  - .geo file FNAME
  - a list of intersections FNAME_INTERSECTIONS
  - a list of every shell's ranges FNAME_MINMAXES in format:
      min_x max_x min_y max_y min_z max_z
      
Options are specified in options.ini, for example like this:

    THICKNESS 0.1 - thickness of 'filler' cylinders
    DISKS_NUM 10 - number of 'filler' and 'shell' particles
    CUBE_EDGE_LENGTH 5 - length of cubic cell representing matrix
    FNAME_INTERSECTIONS results/intersections/11_0.1_5_1_0.15_1.5_10_0 - name of file with the list of intersections
    SHELL_THICKNESS 0.15 - thickness of 'interphase' (full thickness of 'shell' is 2 * SHELL_THICKNESS + THICKNESS)
    FNAME_CLUSTERS results/clusters/11_0.1_5_1_0.15_1.5_10_0
    FNAME_LOG main.log
    FNAME_STRUCTURES_LOG results/structures_log
    TRAJECTORY 0
    FNAME results/geofiles/11_0.1_5_1_0.15_1.5_10_0.geo
    OUTER_RADIUS 1
    FNAME_SEPARATE_LOG results/logs_cpppolygons/11_0.1_5_1_0.15_1.5_10_0
    MAX_ATTEMPTS 100
    FNAME_MINMAXES results/minmaxes/11_0.1_5_1_0.15_1.5_10_0
    VERTICES_NUMBER 6.0


    Ns =  [
        5, 10, 15,          # 15 ~~ 100 steps for L == 5
        20, 25,             # 25 ~~ 1k
        30, 35, 40,         # 40 ~~ 10k
        45, 50, 55,         # 55 ~~ 100k
        60, 65, 70,         # 70 ~~ 1kk
    ]
