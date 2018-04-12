#!/usr/bin/env python3


#LD_LIBRARY_PATH=/home/anton/FEMFolder3/libs:/home/anton/FEMFolder3/my_libs
#export LD_LIBRARY_PATH
#./create_meshes.py


import os
import pprint
pprint = pprint.PrettyPrinter(indent=4).pprint
import shutil
import subprocess
import sys
import time


"""
SizeX 5
SizeY 5
SizeZ 5

MeshFileName mesh.xdr
MaterialsGlobalFileName materials.bin
TaskName test_elas_EYY
G_matrix 1.5
G_interface 30.0
G_filler 232

Strain
0.01 0.0 0.0
0.0 0.0 0.0
0.0 0.0 0.0
"""


def create_fem_main_task(cube_edge_length, axe, structure_name,
                         fname_mesh, fname_bin, task_name,
                         G_matrix, G_interface, G_filler,
                         strain_ratio):
   """
   Creates single axe strain input file.
   """
   zero_strains = '0.0 0.0 0.0\n'
   str_task = ''
   str_task += 'SizeX ' + str(cube_edge_length) +'\n'
   str_task += 'SizeY ' + str(cube_edge_length) +'\n'
   str_task += 'SizeZ ' + str(cube_edge_length) +'\n\n'
   str_task += 'MeshFileName ' + fname_mesh + '\n'
   str_task += 'MaterialsGlobalFileName ' + fname_bin + '\n'
   str_task += 'TaskName ' + task_name + '\n'
   str_task += 'G_matrix ' + str(G_matrix) + '\n'
   str_task += 'G_interface ' + str(G_interface) + '\n'
   str_task += 'G_filler ' + str(G_filler) + '\n\n'
   str_task += 'Strain\n'
   if axe in ['xx', 'XX', 'xX', 'Xx']:
       str_task += str(strain_ratio) + ' 0.0 0.0\n' + 2 * zero_strains
   elif axe in ['yy', 'YY', 'yY', 'Yy']:
       str_task += (zero_strains + '0.0 ' + str(strain_ratio) + ' 0.0\n' +
                    zero_strains)
   elif axe in ['zz', 'ZZ', 'zZ', 'Zz']:
       str_task += 2 * zero_strains + '0.0 0.0 ' + str(strain_ratio) + '\n'
   return str_task


def run_main(stdout, libmesh_exe_folder='/home/anton/FEMFolder3'):
    str_task = create_fem_main_task()
    print(str_task)
    exe_main = libmesh_exe_folder + '/FEM3.x'
    subprocess.call([exe_gen_mesh, ''], stdout=stdout)


def run_process_mesh(stdout, libmesh_exe_folder='/home/anton/FEMFolder3'):
    exe_gen_mesh = libmesh_exe_folder + '/processMesh.x'
    subprocess.call([exe_gen_mesh, ], stdout=stdout)
    return 0


def main(results_folder='mech_results'):
    libmesh_folder = '/home/anton/FEMFolder3'
    folder = results_folder + '/interesting_systems'
    taus = os.listdir(folder)
    params = {tau: [] for tau in taus}
    for tau in taus:
        if not 'bins' in os.listdir(folder + '/' + tau):
            subprocess.call(["mkdir", folder + '/' + tau + '/bins'])
        if not 'logs_process' in os.listdir(folder + '/' + tau):
            subprocess.call(["mkdir", folder + '/' + tau + '/logs_process'])
        if not 'logs_main' in os.listdir(folder + '/' + tau):
            subprocess.call(["mkdir", folder + '/' + tau + '/logs_main'])
        folder_tau = folder + '/' + tau + '/vols'
        vols = os.listdir(folder_tau)
        params[tau].extend([vol.split('_')[3] for vol in vols])
    pprint(params)
    for tau in taus:
        for fi in params[tau]:
            for fname in ['rate_min_fi_' + str(fi), 'rate_max_fi_' + str(fi)]:
                fname_vol = folder + '/' + tau + '/vols/' + fname
                if not fname in os.listdir(folder + '/' + tau + '/vols'):
                    continue
                shutil.copyfile('generated.vol', 'out.mesh')
                process_out = open(folder + '/' + tau + '/logs_process/' + fname,
                                   'w')
                main_out = open(folder + '/' + tau + '/logs_main/' + fname, 'w')
                run_process_mesh(process_out)
                #subprocess.call(["rm", 'out.mesh'])
                #run_main(process_out)


if __name__ == '__main__':
    #main()
    create_fem_main_task(5, 'zz', 'struc',
                         'mesh.xdr', 'materials.bin', 'task_xx',
                         2, 30, 232,
                         0.01)
