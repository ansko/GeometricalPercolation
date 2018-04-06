#!/usr/bin/env python3


import os
import subprocess
from shutil import move

from analyze_clusters_files import (get_clusters_from_files,
                                    analyze_average_clusteriaztion_rate,
                                    analyze_average_cluster_size,
                                    analyze_average_cluster_length)
from create_clusters_files import create_clusters_files
from reparser import reparse


def analyze_clusters():
    f = open('options.ini', 'r')
    for line in f:
        if line.startswith('FNAME '):
            fname_geo = line.split()[1]
        if line.startswith('FNAME_CLUSTERS'):
            fname_clusters = line.split()[1]
        if line.startswith('FNAME_MINMAXES'):
            fname_minmaxes = line.split()[1]
        if line.startswith('SHELL_THICKNESS'):
            sh = float(line.split()[1])
        if line.startswith('THICKNESS'):
            h = float(line.split()[1])
    f = open(fname_geo, 'r')
    actual_particles_number = 0
    for line in f:
        if line.startswith('solid polygonalCylinder'):
            actual_particles_number += 1
    f.close()
    clusters = get_clusters_from_files(fname_clusters, fname_minmaxes)
    rate = analyze_average_clusteriaztion_rate(clusters, actual_particles_number)
    size = analyze_average_cluster_size(clusters) # size in particles
    length = analyze_average_cluster_length(clusters)
    return (rate, size, length)


def run_one_time():
    exe_polygonal = './cpppolygons'
    exe_clusters_creation = './create_clusters_files.py'
    fname_options = 'options.ini'
    with open(fname_options, 'r') as f:
        for line in f:
            if line.startswith('FNAME_LOG'):
                fname_log = line.split()[1]
            if line.startswith('FNAME_MINMAXES'):
                fname_minmaxes = line.split()[1]
            if line.startswith('FNAME_INTERSECTIONS'):
                fname_intersections = line.split()[1]
            if line.startswith('FNAME_CLUSTERS'):
                fname_clusters = line.split()[1]
            if line.startswith('FNAME '):
                fname_geo = line.split()[1]
            if line.startswith('THICKNESS'):
                filler_thickness = line.split()[1]
            if line.startswith('OUTER_RADIUS'):
                filler_outer_r = line.split()[1]
            if line.startswith('MAX_ATTEMPTS'):
                max_attempts = line.split()[1]
            if line.startswith('CUBE_EDGE_LENGTH'):
                edge_length = line.split()[1]
            if line.startswith('DISKS_NUM'):
                fillers_number = line.split()[1]
            if line.startswith('SHELL_THICKNESS'):
                shell_thickness = line.split()[1]
            if line.startswith('VERTICES_NUMBER'):
                vertices_number = line.split()[1]
    subprocess.call([exe_polygonal,])
    fname_reparsed = 'results/reparsed/' + fname_geo[17:-4]
    reparse(fname_geo, fname_reparsed)
    create_clusters_files(fname_intersections, fname_clusters, fname_minmaxes)
    (rate, size, length) = analyze_clusters()
    str_out = ('py: clasterization_rate: ' + '%.2f' % rate + '\n' +
               'py: ave_cluster_size:    ' + '%.2f' % size + '\n' +
               'py: ave_cluster_length:  ' + '%.2f' % length + '\n')
    f = open(fname_log, 'a')
    f.write(str_out)
    return None


def main():
    # checking whether old results exists in folder
    if 'results' in os.listdir():
        print('CRITICAL ERROR:',
              'Folder "results" already exists')
        print('REASON OF EXIT:',
              'You may lose some data')
        return 0
    # configuring
    trajectories = 1
    thicknesses = [0.1, ]
    edges = [5.0, ]
    Rs = [1.0, ]
    shs = [0.15, 0.25, 0.5]
    Ns =  [5, 10, 15, 20, 25, 30, 35, 40]
    fname_log = 'main.log'
    max_attempts = 5
    full_attempts_treshold = 5
    f = open(fname_log, 'w')
    f.write('-----    Main parameters    -----\n')
    f.write('trajectories = ' + str(trajectories) + '\n')
    f.write('thicknesses = ' + str(thicknesses) + '\n')
    f.write('edges = ' + str(edges) + '\n')
    f.write('Rs = ' + str(Rs) + '\n')
    f.write('shs = ' + str(shs) + '\n')
    f.write('Ns = ' + str(Ns) + '\n')
    f.write('---------------------------------\n\n')
    f.close()
    # running
    if not 'results' in os.listdir():
        subprocess.call(["mkdir", "results"])
    if not 'geofiles' in os.listdir('results'):
        subprocess.call(["mkdir", "results/geofiles"])
    if not 'reparsed' in os.listdir('results'):
        subprocess.call(["mkdir", "results/reparsed"])
    if not 'intersections' in os.listdir('results'):
        subprocess.call(["mkdir", "results/intersections"])
    if not 'clusters' in os.listdir('results'):
        subprocess.call(["mkdir", "results/clusters"])
    if not 'minmaxes' in os.listdir('results'):
        subprocess.call(["mkdir", "results/minmaxes"])
    run = 0
    number_of_full_attempts = 0 # number of run where cpppolygons used
                                # all attempts it could have used
    msg_full_attempts = 'WARNING: too high desired filler content' 
    flag_printed = False
    for thickness in thicknesses:
        if flag_printed:
            break
        if number_of_full_attempts ==  full_attempts_treshold:
            print(msg_full_attempts)
            break
        for edge in edges:
            if flag_printed:
                break
            if number_of_full_attempts ==  full_attempts_treshold:
                print(msg_full_attempts)
                flag_printed = True
                break
            for R in Rs:
                if flag_printed:
                    break
                if number_of_full_attempts ==  full_attempts_treshold:
                    print(msg_full_attempts)
                    flag_printed = True
                    break
                for sh in shs:
                    if flag_printed:
                        break
                    if number_of_full_attempts ==  full_attempts_treshold:
                        print(msg_full_attempts)
                        flag_printed = True
                        break
                    tau = '%.1f' % (sh / thickness)
                    for N in Ns:
                        if flag_printed:
                            break
                        if number_of_full_attempts ==  full_attempts_treshold:
                            print(msg_full_attempts)
                            flag_printed = True
                            break
                        for trajectory in range(trajectories):
                            if number_of_full_attempts ==  full_attempts_treshold:
                                print(msg_full_attempts)
                                flag_printed = True
                                break
                            structure_name = ('edge_' + str(int(edge)) +
                                              '_R_' + str(int(R)) +
                                              '_tau_' + tau +
                                              '_N_' + str(int(N)) +
                                              '_trajectory_' +
                                                  str(int(trajectory)))
                            fname_geo = ('results/geofiles/' +
                                         structure_name +
                                         '.geo')
                            fname_intersections = ('results/intersections/' +
                                                   structure_name)
                            fname_clusters = ('results/clusters/' +
                                              structure_name)
                            fname_minmaxes = ('results/minmaxes/' +
                                              structure_name)
                            options = {
                                'FNAME_INTERSECTIONS': fname_intersections,
                                'FNAME_CLUSTERS': fname_clusters,
                                'FNAME_MINMAXES': fname_minmaxes,
                                'THICKNESS': thickness,
                                'CUBE_EDGE_LENGTH': edge,
                                'OUTER_RADIUS': R,
                                'MAX_ATTEMPTS': max_attempts,
                                'VERTICES_NUMBER': 6.0,
                                'SHELL_THICKNESS': sh,
                                'DISKS_NUM': N,
                                'FNAME': fname_geo,
                                'FNAME_LOG': fname_log,
                                'TRAJECTORY': trajectory
                            }
                            f = open('options.ini', 'w')
                            for key in options.keys():
                                str_out = str(key) + ' ' + str(options[key]) + '\n'
                                f.write(str_out)
                            f.close()
                            f = open(fname_log, 'a')
                            f.write('-----    run ' + str(run) + '    -----\n')
                            param_str = 'py: desired system params:\n'
                            keys = ['THICKNESS',
                                    'VERTICES_NUMBER',
                                    'TRAJECTORY',
                                    'CUBE_EDGE_LENGTH',
                                    'OUTER_RADIUS',
                                    'DISKS_NUM',
                            ]
                            for key in keys:
                                str_key = key
                                str_key += (25 - len(key)) * ' '
                                value = float(options[key])
                                if value.is_integer():
                                    value = str(int(value))
                                else:
                                    value = str(value)
                                param_str += str_key + value +'\n'
                            f.write(param_str)
                            f.close()
                            run_one_time()
                            # analyze cpppolygons' attempts number:
                            f = open('main.log', 'r')
                            for line in f:
                                if line.startswith('cpp: Attempts'):
                                    actual_attempts = int(line.split()[2])
                            if actual_attempts == max_attempts:
                                number_of_full_attempts += 1
                            f.close()
                            run += 1
    print('     *****     ')
    if flag_printed or number_of_full_attempts ==  full_attempts_treshold:
        print('Not completely successful run')
    else:
        print('Completely successful run')
    # cleaning folder
    move('main.log', 'results/main.log')
    os.remove('options.ini')
    return 0


main()
