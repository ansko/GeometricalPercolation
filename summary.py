#!/usr/bin/env python3


import os


def summary():
    folder = 'results'
    filenames = os.listdir(folder)
    for filename in filenames:
        if filename.endswith('.geo'):
            system_name = filename[:-4]
            thickness = float(system_name.split('th')[1].split('edge')[0])
            edge = float(system_name.split('edge')[1].split('R')[0])
            R = float(system_name.split('R')[1].split('sh')[0])
            sh = float(system_name.split('sh')[1].split('N')[0])
            N = int(float(system_name.split('N')[1].split('_')[0]))
            i = int(float(system_name.split('_')[1]))
            tau = sh / thickness

            fname_clusters = system_name + '.clusters'
            fname_coords = system_name + '.coords'
            fname_geo = system_name + '.geo'
            fname_intersection = system_name + '.intersections'
            fname_N = system_name + '.props_of_system'
            fname_reparsed = system_name + '.reparsed'

            f = open(folder + '/' + fname_N, 'r')
            for line in f:
                Nreal = int(line)
            if N != Nreal:
                continue

            clusters_number = 0
            ave_cluster_len = 0
            clusterization_rate = 0
            f = open(folder + '/' + fname_clusters, 'r')
            for line in f:
                clusters_number += 1
                ave_cluster_len += len(line.split())
                clusterization_rate += len(line.split())
            if clusters_number > 0:
                ave_cluster_len /= clusters_number
            clusterization_rate /= N

            print('%.2f' % tau,
                  '%.2f' % N,
                  '%.2f' % clusterization_rate,
                  '%.2f' % ave_cluster_len)

summary()
