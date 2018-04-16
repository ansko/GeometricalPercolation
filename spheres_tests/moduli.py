#!/usr/bin/env python3


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
    Calculates Young's moduli
    """
    fnames_moduli = os.listdir(test_results_folder + '/moduli')
    log = open(test_results_folder + '/moduli_log', 'w')
    for fname in fnames_moduli:
        print(fname, end=' ')
        n_chains = int(fname.split('_')[2])
        tau = fname.split('_')[4]
        fi = fname.split('_')[6]
        L = int(fname.split('_')[8])
        f = open(test_results_folder + '/moduli/' + fname, 'r')
        for line in f:
            pass
        if 'XX' in fname:
            idx = 'xx'
            E = float(line.split()[9]) / float(line.split()[0])
        if 'YY' in fname:
            idx = 'yy'
            E = float(line.split()[13]) / float(line.split()[4])
        if 'ZZ' in fname:
            idx = 'zz'
            E = float(line.split()[17]) / float(line.split()[8])
        E *= 0.52 / 0.7
        print(E)
        log.write('tau ' + tau + ' fi ' + fi + ' E' + idx + ' ' + str(E) + '\n')


if __name__ == '__main__':
    main()
