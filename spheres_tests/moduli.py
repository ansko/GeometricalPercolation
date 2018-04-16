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
    irregs = {}
    percs = {}

    fnames_moduli = os.listdir(test_results_folder + '/moduli')
    log = open(test_results_folder + '/moduli_log', 'w')
    for fname in fnames_moduli:
        struc_type = fname.split('_')[0]
        fi = fname.split('_')[1]
        f = open(test_results_folder + '/moduli/' + fname, 'r')
        for line in f:
            pass
        if 'XX' in fname:
            idx = 'xx'
            E = 0.52 / 0.7 * float(line.split()[9]) / float(line.split()[0])
        if 'YY' in fname:
            idx = 'yy'
            E = 0.52 / 0.7 * float(line.split()[13]) / float(line.split()[4])
        if 'ZZ' in fname:
            idx = 'zz'
            E = 0.52 / 0.7 * float(line.split()[17]) / float(line.split()[8])
        if struc_type == 'irreg':
            if fi in irregs.keys():
                if idx == 'xx':
                    irregs[fi][0] = E
                elif idx == 'yy':
                    irregs[fi][1] = E
                elif idx == 'zz':
                    irregs[fi][2] = E
                else:
                    print('unknown idx')
                    return None
            else:
                if idx == 'xx':
                    irregs[fi] = [E, 0, 0]
                elif idx =='yy':
                    irregs[fi] = [0, E, 0]
                elif idx == 'zz':
                    irregs[fi] = [0, 0, E]
                else:
                    print('unknown idx')
                    return None
        elif struc_type == 'per':
            if fi in percs.keys():
                if idx == 'xx':
                    percs[fi][0] = E
                elif idx == 'yy':
                    percs[fi][1] = E
                elif idx == 'zz':
                    percs[fi][2] = E
                else:
                    print('unknown idx')
                    return None
            else:
                if idx == 'xx':
                    percs[fi] = [E, 0, 0]
                elif idx =='yy':
                    percs[fi] = [0, E, 0]
                elif idx == 'zz':
                    percs[fi] = [0, 0, E]
                else:
                    print('unknown idx')
                    return None
        else:
            print('unknown structure type')
            return None
        log.write('struc_type ' + struc_type + ' fi ' + fi + ' E' + idx + ' ' + str(E) + '\n')
    f.close()
    str_heading = 'fi Exx Eyy Ezz Eave\n'
    f = open(test_results_folder + '/moduli_perc', 'w')
    f.write(str_heading)
    for key in sorted(list(percs.keys())):
        Exx = percs[key][0]
        Eyy = percs[key][1]
        Ezz = percs[key][2]
        E = (Exx + Eyy + Ezz) / 3
        str_out = ' '.join([str(key), str(Exx), str(Eyy), str(Ezz), str(E)])
        f.write(str_out + '\n')
    f.close()
    f = open(test_results_folder + '/moduli_irreg', 'w')
    f.write(str_heading)
    for key in sorted(list(irregs.keys())):
        Exx = irregs[key][0]
        Eyy = irregs[key][1]
        Ezz = irregs[key][2]
        E = (Exx + Eyy + Ezz) / 3
        str_out = ' '.join([str(key), str(Exx), str(Eyy), str(Ezz), str(E)])
        f.write(str_out + '\n')
    f.close()

if __name__ == '__main__':
    main()
