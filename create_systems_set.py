#!/usr/bin/env python3


import os
import shutil
import subprocess
import time

from intersections_to_clusters import (intersections_to_clusters,
                                       single_file_conversion)
from get_cluster_lengths import calculate_lengths


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
    return None


def create_systems_set(results_folder='results'):
    # checking whether old results exists in folder
    if results_folder in os.listdir():
        print('CRITICAL ERROR:',
              'Folder "results" already exists')
        print('REASON OF EXIT:',
              'You may lose some data')
        return 0
    program_start_time = time.time()
    # configuring
        # vertices number
    n = 6
######### Key parameter
        # MAX_ATTEMPTS in cpppolygons
#########
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
    Ns = [5 * i for i in range(1, Ns_num)]
    consecutive_unsuccessful_runs_number = 1 # Number of consecutive unsuccessful
                                             # attempts to place specified fillers
    if max_attempts < 10000:
        consecutive_unsuccessful_runs_number = 10
    if max_attempts < 1000:
        consecutive_unsuccessful_runs_number = 100
    if max_attempts < 100:
        consecutive_unsuccessful_runs_number = 1000
    fname_structures_log = results_folder + '/structures_log'
    fname_log = 'main.log'
    trajectories = 10
    thicknesses = [0.1, ]
    edges = [5, 10, 15, 20, 25]
    Rs = [1, ]
    shs = [0.15, 0.25, 0.5]
    f = open(fname_log, 'w')
    f.write('-----    Main parameters    -----\n')
    f.write('tra: ' + str(trajectories) + '\n')
    f.write('hs:  ' + str(thicknesses) + '\n')
    f.write('max_attempts = ' + str(max_attempts) + '\n')
    f.write('Ls:  ' + str(edges) + '\n')
    f.write('Rs:  ' + str(Rs) + '\n')
    f.write('shs: ' + str(shs) + '\n')
    f.write('Ns:  ' + str(Ns) + '\n')
    f.write('---------------------------------\n')
    f.close()
    # preparing for runs
    if not 'results' in os.listdir():
        subprocess.call(["mkdir", results_folder])
    if not 'geofiles' in os.listdir(results_folder):
        subprocess.call(["mkdir", results_folder + "/geofiles"])
    if not 'reparsed' in os.listdir(results_folder):
        subprocess.call(["mkdir", results_folder + "/reparsed"])
    if not 'intersections' in os.listdir(results_folder):
        subprocess.call(["mkdir", results_folder + "/intersections"])
    if not 'clusters' in os.listdir(results_folder):
        subprocess.call(["mkdir", results_folder + "/clusters"])
    if not 'minmaxes' in os.listdir(results_folder):
        subprocess.call(["mkdir", results_folder + "/minmaxes"])
    if not 'logs_cpppolygons' in os.listdir(results_folder):
        subprocess.call(["mkdir", results_folder + "/logs_cpppolygons"])
    if not 'py_logs' in os.listdir(results_folder):
        subprocess.call(["mkdir", results_folder + "/py_logs"])
    if not 'clusters_lengths' in os.listdir(results_folder):
        subprocess.call(["mkdir", results_folder + "/clusters_lengths"])
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
    print('-----    Main parameters    -----')
    print('tra:     ', int(trajectories))
    print('hs:      ', *['%.1f' % h for h in thicknesses])
    print('max_att: ', int(max_attempts))
    print('Ls:      ', *[int(L) for L in edges])
    print('Rs:      ', *[int(R) for R in Rs])
    print('shs:     ', *['%.2f' % sh for sh in shs])
    print('Ns:      ', *['%.2f' % N for N in Ns])
    print('***')
    print('consecutive unsuccessful runs', consecutive_unsuccessful_runs_number)
    print('---------------------------------')
    # running
    run = 0
    skipped = 0
    unsuccess = 0
    old_L_value = 0 # Value of L at wich specified  number of fillers
                    # was impossible to be placed.
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
        print('+' + str(run) + ' -' + str(skipped) + ';',
              str(int(100 * (run + skipped + 1) / runs_num)) + '%',
              'last step', last_iteration_time,
              'passed', int(ongoing_time),
              'left', appro_last_time, 'sec')
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
        fname_py_log = results_folder + '/py_logs/' + structure_name
        fname_geo = results_folder + '/geofiles/' + structure_name + '.geo'
        fname_intersections = results_folder + '/intersections/' + structure_name
        fname_clusters = results_folder + '/clusters/' + structure_name
        fname_minmaxes = results_folder + '/minmaxes/' + structure_name
        cpp_output = results_folder + '/logs_cpppolygons/' + structure_name
        options = {
            'STRUCTURE': structure_name,
            'FNAME_SEPARATE_LOG': cpp_output,
            'FNAME_INTERSECTIONS': fname_intersections,
            'FNAME_CLUSTERS': fname_clusters,
            'FNAME_MINMAXES': fname_minmaxes,
            'THICKNESS': h,
            'CUBE_EDGE_LENGTH': L,
            'OUTER_RADIUS': R,
            'MAX_ATTEMPTS': max_attempts,
            'VERTICES_NUMBER': n,
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
######## run
        run_one_time()
        single_file_conversion(results_folder, structure_name)  # int -> clusters
        calculate_lengths(results_folder)
########
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
    print('tra:     ', int(trajectories))
    print('hs:      ', *['%.1f' % h for h in thicknesses])
    print('max_att: ', int(max_attempts))
    print('Ls:      ', *[int(L) for L in edges])
    print('Rs:      ', *[int(R) for R in Rs])
    print('shs:     ', *['%.2f' % sh for sh in shs])
    print('Ns:      ', *['%.2f' % N for N in Ns])
    print('---------------------------------')
    print('Working time:', int(time.time() - program_start_time), 'seconds')
    return 0


create_systems_set()
