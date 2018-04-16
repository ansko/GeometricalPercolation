#!/usr/bin/env python3


# LD_LIBRARY_PATH=/home/anton/FEMFolder3/libs:/home/anton/FEMFolder3/my_libs
# export LD_LIBRARY_PATH


import os
import pprint
pprint = pprint.PrettyPrinter(indent=4).pprint
import shutil
import subprocess
import sys
import time


test_results_folder = 'results'


def main(libmesh_exe_folder='/home/anton/FEMFolder3',
         test_results_folder=test_results_folder):
    """
    Creates files for FEMmain by calling fem_process.
    """
    # subprocess.call(['rm', '-rf', test_results_folder + '/bins'])
    # subprocess.call(['rm', '-rf', test_results_folder + '/logs_process'])
    if 'bins' in os.listdir():
        print('error in create_bins.py:',
              'bins folder exists')
        return None
    if 'logs_process' in os.listdir():
        print('error in create_bins.py:',
              'logs_process folder exists')
        return None
    exe_process = libmesh_exe_folder + '/processMesh.x'
    log = open(test_results_folder + '/meshes_processings_log', 'w')
    subprocess.call(['mkdir', test_results_folder + '/bins'])
    subprocess.call(['mkdir', test_results_folder + '/logs_process'])
    fnames_vol = os.listdir(test_results_folder + '/meshes')
    for fname in fnames_vol:
        shutil.copyfile(test_results_folder + '/meshes/' + fname, 'out.mesh')
        log.write(fname + '\n')
        print(fname)
        f = open(test_results_folder + '/logs_process/' + fname, 'w')
        code = subprocess.call([exe_process, test_results_folder + '/meshes/' +
                                fname], stdout=f)
        bin_name = fname[:-3] + 'bin'
        shutil.copyfile('materials.bin',
                        test_results_folder + '/bins/' + vol_name)


if __name__ == '__main__':
    main()
