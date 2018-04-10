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
            if line.startswith('FNAME_PY_LOG'):
                fname_py_log = line.split()[1]
            if line.startswith('FNAME_STRUCTURES_LOG'):
                fname_structures_log = line.split()[1]
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
    str_out = ('clu_rate:' + '%.2f' % rate +
               ':ave_clu_size:' + '%.2f' % size +
               ':ave_clu_len:' + '%.2f' % length)
    f = open(fname_py_log, 'w')
    f.write(str_out)
    f.close()
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
    consecutive_unsuccessful_runs_number = 3
    fname_structures_log = 'results/structures_log'
    fname_log = 'main.log'
    trajectories = 10
    thicknesses = [0.1, ]
    edges = [5, 10, 15, 20, 25]
    Rs = [1, ]
    shs = [0.15, 0.25, 0.5]
    Ns =  [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
    max_attempts = 10000
    full_attempts_treshold = 5
    f = open(fname_log, 'w')
    f.write('-----    Main parameters    -----\n')
    f.write('trajectories = ' + str(trajectories) + '\n')
    f.write('thicknesses = ' + str(thicknesses) + '\n')
    f.write('edges = ' + str(edges) + '\n')
    f.write('Rs = ' + str(Rs) + '\n')
    f.write('shs = ' + str(shs) + '\n')
    f.write('Ns = ' + str(Ns) + '\n')
    f.write('---------------------------------\n')
    f.close()
    # preparing for runs
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
    if not 'logs_cpppolygons' in os.listdir('results'):
        subprocess.call(["mkdir", "results/logs_cpppolygons"])
    if not 'py_logs' in os.listdir('results'):
        subprocess.call(["mkdir", "results/py_logs"])
    runs_num = 0
    parameters_sets = []
    for thickness in thicknesses:
        for edge in edges:
            for R in Rs:
                for sh in shs:
                    tau = '%.1f' % (sh / thickness)
                    for N in Ns:
                        for trajectory in range(trajectories):
                            parameters_sets.append({
                                'h': thickness,
                                'L': edge,
                                'R': R,
                                'sh': sh,
                                'tau': tau,
                                'N': N,
                                'tra': trajectory
                            })
                            runs_num += 1
    # running
    run = 0
    skipped = 0
    unsuccess = 0
    flag = False
    old_L_value = 0
    for parameter_set in parameters_sets:
        print('run', run, 'skipped', skipped, 'at all', run + skipped,
              '/', runs_num, 'runs')
        if unsuccess == consecutive_unsuccessful_runs_number:
            # should go to next L value
            old_L_value = L # now all Ls should be greater than this value
            unsuccess = 0
            skipped += 1
            continue
        L = parameter_set['L']
        if not L > old_L_value:
            skipped += 1
            continue
        run += 1
        h = parameter_set['h']
        R = parameter_set['R'] 
        sh = parameter_set['sh']
        tau = parameter_set['tau']
        N = parameter_set['N']
        tra = parameter_set['tra']
        structure_name = '_'.join([str(word) for word in [run, h, L, R, sh, tau,
                                                          N, tra]])
        fname_py_log = 'results/py_logs/' + structure_name
        fname_geo = 'results/geofiles/' + structure_name + '.geo'
        fname_intersections = 'results/intersections/' + structure_name
        fname_clusters = 'results/clusters/' + structure_name
        fname_minmaxes = 'results/minmaxes/' + structure_name
        cpp_output = 'results/logs_cpppolygons/' + structure_name
        options = {
            'FNAME_PY_LOG': fname_py_log,
            'FNAME_SEPARATE_LOG': cpp_output,
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
            'FNAME_LOG': cpp_output,
            'TRAJECTORY': trajectory,
            'FNAME_STRUCTURES_LOG': fname_structures_log,
            'FNAME_LOG': fname_log
        }
        f = open('options.ini', 'w')
        for key in options.keys():
            str_out = str(key) + ' ' + str(options[key]) + '\n'
            f.write(str_out)
        f.close()
        run_one_time()
        str_out = 'structure_name:' + structure_name + ':'
        for parameter in parameter_set:
            str_out += str(parameter) + ':' + str(parameter_set[parameter]) + ':'
        str_out = str_out[:-1] + '\n'
        f = open(fname_structures_log, 'a')
        f.write(str_out)
        f.close()
        # analyze cpppolygons' attempts number:
        f = open(cpp_output, 'r')
        real_N = int(f.readline().split(':')[3])
        if real_N < N:
            unsuccess += 1
    # cleaning folder
    move('main.log', 'results/main.log')
    os.remove('options.ini')
    return 0


main()
