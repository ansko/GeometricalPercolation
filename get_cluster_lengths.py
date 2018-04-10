#!/usr/bin/env python3


import os
import subprocess


results_folder = 'results100k'


def calculate_lengths(results_folder):
    fnames = os.listdir(results_folder + '/clusters')
    for structure_name in fnames:
        L = float(structure_name.split('_')[2])
        minmaxes = []
        f = open(results_folder + '/minmaxes/' + structure_name, 'r')
        for line in f:
            minmaxes.append([
                float(line.split()[0]),
                float(line.split()[1]),
                float(line.split()[2]),
                float(line.split()[3]),
                float(line.split()[4]),
                float(line.split()[5])
            ])
        f = open(results_folder + '/clusters/' + structure_name, 'r')
        flen = open(results_folder + '/clusters_lengths/' + structure_name,
                    'w')
        for line in f:
            minx = L
            miny = L
            minz = L
            maxx = 0
            maxy = 0
            maxz = 0
            ls = line.split()
            for particle in ls:
                particle = int(particle)
                minx = min(minx, max(0, minmaxes[particle][0]))
                miny = min(miny, max(0, minmaxes[particle][2]))
                minz = min(minz, max(0, minmaxes[particle][4]))
                maxx = max(maxx, min(L, minmaxes[particle][1]))
                maxy = max(maxy, min(L, minmaxes[particle][3]))
                maxz = max(maxz, min(L, minmaxes[particle][5]))
            xlen = maxx - minx
            ylen = maxy - miny
            zlen = maxz - minz
            ave_len = (xlen + ylen + zlen) / 3
            str_out = ' '.join([str(xlen), str(ylen), str(zlen), str(ave_len)])
            flen.write(str_out + '\n')
    return


if __name__ == '__main__':
    calculate_lengths()
