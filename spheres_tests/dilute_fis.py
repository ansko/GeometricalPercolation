#!/usr/bin/env python3


import os
import pprint
pprint=pprint.PrettyPrinter(indent=4).pprint
import shutil


folder_per = 'results/geo/per'
folder_irreg = 'results/geo/irreg'
fis = []


diluted_fis = [
    0.0010336922542189507,
    0.0020257576661745743,
    0.0029503345802009617,
    0.0039693982553796765,
    0.0046892623908660995,
    0.005624235782332101,
    0.006869371691522871,
    0.008578642339402528,
    0.011014850275546481,
    0.014656796167790259,
    0.020453077171808547,
    0.030505527208275943,
    0.05026548245743669
]


fnames_per = 0
for fname_per in os.listdir(folder_per):
    fi = float(fname_per[:-4].split('_')[5])
    if fi in diluted_fis:
        fnames_per += 1


fnames_irreg = 0
for fname_irreg in os.listdir(folder_irreg):
    fi = float(fname_irreg[:-4].split('_')[5])
    if fi in diluted_fis:
        fnames_irreg += 1


def remove_geos():
    for folder in [folder_per, folder_irreg]:
        for fname in os.listdir(folder):
            fi = float(fname[:-4].split('_')[5])
            print(fi)
            if fi not in diluted_fis:
                os.remove(folder + '/' + fname)



#print(fnames_per, fnames_irreg) # same numbers if fi's are
                                # the same in both folders

#if fnames_per == fnames_irreg:
#    remove_geos()
