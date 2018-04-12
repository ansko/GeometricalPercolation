#!/usr/bin/env python3


import os
import pprint
pprint = pprint.PrettyPrinter(indent=4).pprint
import shutil
import subprocess
import sys
import time


from db_analysis import get_db


def chose_interesting(results_folder='mech_results'):
    """
    Finds in database systems with same fi and tau values
    but having dramatically different crystallization_rate.
    """
    db = get_db()
    taus = set()
    fis = set()
    for entry in db:
        taus.add(float(entry['tau']))
        fis.add(float(entry['fi']))
    taus = sorted(list(taus))
    fis = sorted(list(fis))
    rates = {
        tau: {
            fi: [
                1, 0, '', '' # min_rate, max_rate,
                             # strucutre_name for min and max
                             # will be stored here after.
            ] for fi in fis
        } for tau in taus
    }
    for entry in db:
        tau = float(entry['tau'])
        fi = float(entry['fi'])
        rate = float(entry['clusterization_rate'])
        structure_name = entry['structure_name']
        if rates[tau][fi][0] >= rate: 
            rates[tau][fi][0] = rate
            rates[tau][fi][2] = structure_name
        if rates[tau][fi][1] <= rate:
            rates[tau][fi][1] = max(rates[tau][fi][1], rate)
            rates[tau][fi][3] = structure_name
    f = open(results_folder + '/interesting_systems.log', 'w')
    str_out = ' '.join(['tau', 'fi', 'fname_with_min_clusterization_rate',
                        'fname_with_min_clusterization_rate'])
    f.write(str_out + '\n')
    for tau in rates.keys():
        for fi in sorted(list(rates[tau].keys())):
            f.write(' '.join([str(tau),
                              str(fi),
                              str(rates[tau][fi][2]), 
                              str(rates[tau][fi][3]),
                              '\n']))


def cp_interesting_files(results_folder='mech_results'):
    """
    Copies chosen in chose_interesting files .geo from results/geofiles
    into mech_results/geo
    """
    if 'interesting_systems' in os.listdir(results_folder):
        print('Error in cp_interesting_files:',
              'directory with interesting files already exists')
        return None
    subprocess.call(["mkdir", results_folder + '/interesting_systems'])
    f = open(results_folder + '/interesting_systems.log', 'r')
    for line in f:
        if line.startswith('tau'): # it is heading
            continue
        if len(line.split()) != 4:
            print('Error in cp_interesting_files:',
                  'not all files are found')
            return None
        tau = float(line.split()[0])
        fi = float(line.split()[1])
        min_rate_fname = line.split()[2] + '.geo'
        max_rate_fname = line.split()[3] + '.geo'
        tmp = results_folder + '/interesting_systems/tau_' + str(tau) + '/geo'
        min_name = tmp + '/rate_min_fi_' + str(fi)
        max_name = tmp + '/rate_max_fi_' + str(fi)
        if not 'tau_' + str(tau) in (os.listdir(results_folder +
                                    '/interesting_systems')):
            subprocess.call(["mkdir", tmp[:-4]])
            subprocess.call(["mkdir", tmp])
        shutil.copyfile('results/geofiles/' + min_rate_fname, min_name)
        shutil.copyfile('results/geofiles/' + max_rate_fname, max_name)


def create_meshes(results_folder='mech_results',
                  libmesh_exe_folder='/home/anton/FEMFolder3'):
    """
    Performs meshing for all .geo files from
    mech_results/geo
    """
    exe_gen_mesh = libmesh_exe_folder + '/gen_mesh.x'
    log = open(results_folder + '/create_meshes.log', 'w')
    taus = os.listdir(results_folder + '/interesting_systems')
    run = 0
    all_runs = 0
    for tau in taus:
        fnames = os.listdir(results_folder +
                            '/interesting_systems/' + tau + '/geo')
        all_runs += len(fnames)
    for tau in taus:
        fnames = os.listdir(results_folder +
                            '/interesting_systems/' + tau + '/geo')
        vol_folder = results_folder + '/interesting_systems/' + tau + '/vols'
        mesher_folder = (results_folder + '/interesting_systems/' + tau +
                         '/logs_gen_mesh')
        subprocess.call(["mkdir", vol_folder])
        subprocess.call(["mkdir", mesher_folder])
        for fname in fnames:
            run += 1
            str_out = ' '.join(['run', str(run), '/', str(all_runs)])
            print(str_out)
            log.write(str_out + '\n')
            shutil.copyfile((results_folder +
                             '/interesting_systems/' + tau + '/geo/' + fname),
                            libmesh_exe_folder + '/script/' + fname + '.geo')
            mesher_log = open(mesher_folder + '/' + fname + '.log', 'w')
            mesher_start_time = time.time()
            gen_mesh_code = subprocess.call([exe_gen_mesh,
                                    libmesh_exe_folder + '/script/' + fname +
                                    '.geo', '0.15', '2', '2'],
                                 stdout=mesher_log)
            mesher_run_time = time.time() - mesher_start_time
            str_out = ' '.join(['mesher_run_time:', str(mesher_run_time),
                                'return code:', str(gen_mesh_code)])
            print(str_out)
            log.write(str_out + '\n')
            if gen_mesh_code == 0:
                shutil.copyfile('generated.vol',
                                results_folder +
                                '/interesting_systems/' + tau + '/vols/' + fname)


def main(results_folder='mech_results'):
    """
    Choses intersting structures in database and meshes them.
    """
    subprocess.call(["rm", '-rf', results_folder])
    if results_folder in os.listdir():
        print('CRITICAL ERROR:',
              'Folder "mech_results" already exists')
        print('REASON OF EXIT:',
              'You may lose some data')
        return 0
    subprocess.call(["mkdir", results_folder])
    chose_interesting()
    cp_interesting_files()
    create_meshes()


if __name__ == '__main__':
    main()
