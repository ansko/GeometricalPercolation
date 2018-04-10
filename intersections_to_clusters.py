#!/usr/bin/env python3


import os
import pprint
pprint=pprint.PrettyPrinter(indent=4).pprint
import subprocess


def intersections_to_clusters(results_folder):
    """
    Clusterizes all intersections.
    """
    intersections = []
    clusters = []
    folder = results_folder + '/intersections'
    fnames = os.listdir(folder)
    i = 0
    try:
        subprocess.call(["mkdir", results_folder + "/new_clusters"])
    except:
        pass
    for fname in fnames:#['406_0.1_25_1_0.15_1.5_2500_3', ]:
        i += 1
        print(i, len(fnames))
        single_file_conversion(fname)


def single_file_conversion(results_folder, fname):
    """
    For file fname with intersection makes file with clusters.
    """
    intersections = []
    f = open(results_folder + '/intersections/' + fname, 'r')
    for line in f:
        intersections.append([int(line.split()[0]), int(line.split()[1])])
    arr = []
    for intersection in intersections:
        flag = False
        for a in arr:
            if intersection[0] in a:
                a.add(intersection[1])
                flag = True
            if intersection[1] in a:
                a.add(intersection[0])
                flag = True
        if not flag:
            arr.append(set(intersection))
    to_remove = set()
    for i, a in enumerate(arr):
        for j, b in enumerate(arr):
            if j <= i:
                continue
            for particle in a:
                if particle in b:
                    to_remove.add(j)
    result = [arr[i] for i in set(range(len(arr))) - to_remove]
    f = open(results_folder + '/clusters/' + fname, 'w')
    for cluster in result:
        cluster = set(cluster)
        str_out = ''
        for particle in cluster:
            str_out += str(particle) + ' '
        f.write(str_out[:-1] + '\n')
    return None


if __name__ == '__main__':
    intersections_to_clusters()
