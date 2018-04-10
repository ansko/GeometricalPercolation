#!/usr/bin/env python3


import os
import shutil
import subprocess
import time


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
    """
    # checking whether old results exists in folder
    if 'results' in os.listdir():
        print('CRITICAL ERROR:',
              'Folder "results" already exists')
        print('REASON OF EXIT:',
              'You may lose some data')
        return 0
    """
    program_start_time = time.time()
    # configuring
      # vertices number
    n = 6
      # MAX_ATTEMPTS in cpppolygons
    max_attempts = 100000
      # adjusting N
    if max_attempts < 1000000:
        Ns_num = 12 
    if max_attempts < 100000:
        Ns_num = 9
    if max_attempts < 10000:
        Ns_num = 8
    if max_attempts < 1000:
        Ns_num = 5
    if max_attempts < 100:
        Ns_num = 3
    # Ns =  [
    #     5, 10, 15,          # 15 ~~ 100 steps for L == 5
    #     20, 25,             # 25 ~~ 1k
    #     30, 35, 40,         # 40 ~~ 10k
    #     45, 50, 55,         # 55 ~~ 100k
    #     60, 65, 70,         # 70 ~~ 1kk
    # ]
    Ns = [5 * i for i in range(1, Ns_num)]          # ...
    consecutive_unsuccessful_runs_number = 3
    fname_structures_log = 'results/structures_log'
    fname_log = 'main.log'
    trajectories = 10
    thicknesses = [0.1, ]
    edges = [5, 10, 15, 20, 25]
    Rs = [1, ]
    shs = [0.15, 0.25, 0.5]
    f = open(fname_log, 'w')
    f.write('-----    Main parameters    -----\n')
    f.write('trajectories = ' + str(trajectories) + '\n')
    f.write('thicknesses = ' + str(thicknesses) + '\n')
    f.write('max_attempts = ' + str(max_attempts) + '\n')
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
    loop_start_time = time.time()
    last_iteration_time = None
    appro_last_time = 'infty'
    for parameter_set in parameters_sets:
        iteration_start_time = time.time()
        if last_iteration_time is not None and str(last_iteration_time) != '0.0':
            last_iteration_time = '%.1f' % (0.000001 + float(last_iteration_time))
        ongoing_time = time.time() - program_start_time
        if runs_num - run - skipped != 0 and run + skipped != 0:
            appro_last_time = (runs_num - run - skipped) / (run + skipped)
            appro_last_time *= ongoing_time
        if not appro_last_time == 'infty':
            appro_last_time = int(appro_last_time)
        print('run', run, 'skipped', skipped, 'done',
              str(int(100 * (run + skipped + 1) / runs_num)) + '%',
              'last iteration', last_iteration_time,
              'passed', int(ongoing_time),
              'last', appro_last_time, 'sec')
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
        L = parameter_set['L']
        N *= (int(L / 5))**3   # Scaling of N for Ls greater than 5
                               # because Ns is written for L == 5.
                               # Seems to work properly.
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
            'THICKNESS': h,
            'CUBE_EDGE_LENGTH': L,
            'OUTER_RADIUS': R,
            'MAX_ATTEMPTS': max_attempts,
            'VERTICES_NUMBER': 6.0,
            'SHELL_THICKNESS': sh,
            'DISKS_NUM': N,
            'FNAME': fname_geo,
            'FNAME_LOG': cpp_output,
            'TRAJECTORY': tra,
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
        iteration_end_time = time.time()
        last_iteration_time = iteration_end_time - iteration_start_time
    # cleaning folder
    shutil.move('main.log', 'results/main.log')
    os.remove('options.ini')
    # recalling the parameters in console
    print('-----    Main parameters    -----')
    print('traj num:', int(trajectories))
    print('hs:      ', *['%.1f' % h for h in thicknesses])
    print('max_att: ', int(max_attempts))
    print('Ls:      ', *[int(L) for L in edges])
    print('Rs:      ', *[int(R) for R in Rs])
    print('shs:     ', *['%.2f' % sh for sh in shs])
    print('Ns:      ', *['%.2f' % N for N in Ns])
    print('---------------------------------')
    print('Working time:', int(time.time() - program_start_time), 'seconds')
    return 0


main()
