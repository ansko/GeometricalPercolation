#!/usr/bin/env python3


import subprocess
from shutil import copyfile

from analyze_clusters_files import (get_clusters_from_files,
                                    analyze_average_clusteriaztion_rate,
                                    analyze_average_cluster_size,
                                    analyze_average_cluster_length)


def analyze_clusters():
    f = open('options.ini', 'r')
    for line in f:
        if line.startswith('THICKNESS'):
            h = float(line.split()[1])
        if line.startswith('SHELL_THICKNESS'):
            sh = float(line.split()[1])
        if line.startswith('CUBE_EDGE_LENGTH'):
            edge_len = float(line.split()[1])
        if line.startswith('OUTER_RADIUS'):
            filler_R = float(line.split()[1])
    f = open('1.geo', 'r')
    N = 0
    for line in f:
        if line.startswith('solid polygonalCylinder'):
            N += 1
    tau = str(sh / h)
    if tau == '5.0':
        tau = '5'
    clusters = get_clusters_from_files(tau, N, edge_len)
    rate = analyze_average_clusteriaztion_rate(clusters, filler_R, h, N)
    size = analyze_average_cluster_size(clusters) # size in particles
    length = analyze_average_cluster_length(clusters)
    return (rate, size, length)


def runNtimes(Ntimes, log_name):
    exe_polygonal = './create_system_intersections_coords_new'
    exe_reparser = './reparser.py'
    exe_clusters_creation = './create_clusters_files.py'
    heading = 'clusterization_rate ave_cluster_size ave_cluster_length N\n'
    general_log_name = log_name
    f = open(general_log_name, 'w')
    f.write('log for:\ncell_size = 5.0\n' +
                      'shell_thickness = 0.5\n' +
                      'thickness = 0.1\n' +
                      'outer_radius = 1\n' +
                      'vertices_number = 6\n' +
                      'attempts = 1000\n' +
                      'disks_num = 50\n')
    f.write(heading)
    for i in range(Ntimes):
        subprocess.call([exe_polygonal,])
        subprocess.call([exe_reparser,])
        subprocess.call([exe_clusters_creation,])
        (rate, size, length) = analyze_clusters()
        str_out = '%.2f' % rate + '\t' + '%.2f' % size + '\t' + '%.2f' % length
        fin = open('props_of_system', 'r')
        for line in fin:
            pass
        str_out += '\t' + line + '\n'
        f.write(str_out)
        sname = log_name[4:]
        copyfile('1.geo', 'results/' + sname + '_' + str(i) + '.geo')
        copyfile('clusters', 'results/' + sname + '_' + str(i) + '.clusters')
        copyfile('coords.log', 'results/' + sname + '_' + str(i) + '.coords')
        copyfile('intersections.log', 'results/' + sname + '_' + str(i) +
                 '.intersections')
        copyfile('props_of_system', 'results/' + sname + '_' + str(i) +
                 '.props_of_system')
        copyfile('reparsed', 'results/' + sname + '_' + str(i) + '.reparsed')


def main():
    Ntimes = 10
    thicknesses = [0.1, ]
    edges = [5.0, ]
    Rs = [1.0, ]
    shs = [0.15, 0.25, 0.5]
    Ns =  [5, 10, 15, 20, 25, 30, 35, 40] 
    params_runner = open('params_runner.log', 'w')
    params_runner.write('Ntimes = ' + str(Ntimes) + '\n')
    params_runner.write('thicknesses = ' + str(thicknesses) + '\n')
    params_runner.write('edges = ' + str(edges) + '\n')
    params_runner.write('Rs = ' + str(Rs) + '\n')
    params_runner.write('shs = ' + str(shs) + '\n')
    params_runner.write('Ns = ' + str(Ns) + '\n')
    for thickness in thicknesses:
        for edge in edges:
            for R in Rs:
                for sh in shs:
                    for N in Ns:
                        options = {
                            'THICKNESS': thickness,
                            'CUBE_EDGE_LENGTH': edge,
                            'OUTER_RADIUS': R,
                            'MAX_ATTEMPTS': 1000.0,
                            'VERTICES_NUMBER': 6.0,
                            'SHELL_THICKNESS': sh,
                            'DISKS_NUM': N,
                            'FNAME': '1.geo'
                        }
                        f = open('options.ini', 'w')
                        for key in options.keys():
                            str_out = str(key) + ' ' + str(options[key]) + '\n'
                            f.write(str_out)
                        f.close()
                        log_name = ('log_' +
                                    'th' + '%.2f' % thickness +
                                    'edge' + '%.2f' % edge +
                                    'R' + '%.2f' % R +
                                    'sh' + '%.2f' % sh +
                                    'N' + '%.2f' % N)
                        runNtimes(Ntimes, log_name)


main()
