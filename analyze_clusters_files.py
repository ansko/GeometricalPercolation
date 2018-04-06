#!/usr/bin/env python3


import copy
import math

import pprint
pprint=pprint.PrettyPrinter(indent=4).pprint


def get_clusters_from_files(tau, N, edge_len):
    entry_empty = {'cluster_size': None,
                   'cluster_x_len': None,
                   'cluster_y_len': None,
                   'cluster_z_len': None,
                   'particles': []}
    clusters = []
    entries = []
    if True:
        if True:
            if True:
                # analyzing file with list of clusters in the system
                fname = 'clusters'#culster_folder + '/' + system_name
                fin = open(fname, 'r')
                for line in fin:
                    ls = line.split()
                    if len(ls) < 2:
                        continue
                    cluster = [int(ls[i]) for i in range(len(ls))]
                    clusters.append(cluster)
                for cluster in clusters:
                    entry = copy.deepcopy(entry_empty)
                    entry['cluster_size'] = len(cluster)
                    entry['particles'] = cluster
                    entries.append(entry)
    if True:
        if True:
            if True:
                # analyzing file with particle minmaxes
                fname = 'coords.log'
                fin = open(fname, 'r')
                minmaxes = []
                for line in fin:
                    ls = line.split(' ') # number:minx:miny:minz:maxx:maxy:maxz
                    minmaxes.append([float(ls[0]), float(ls[1]), float(ls[2]),
                                     float(ls[3]), float(ls[4]), float(ls[5])])
                # calculating every cluster's size
                for cluster in entries:
                    min_x = edge_len
                    min_y = edge_len
                    min_z = edge_len
                    max_x = 0
                    max_y = 0
                    max_z = 0
                    for particle in cluster['particles']:
                        min_x = min(min_x, minmaxes[particle][0])
                        min_y = min(min_y, minmaxes[particle][1])
                        min_z = min(min_z, minmaxes[particle][2])
                        max_x = max(max_x, minmaxes[particle][3])
                        max_y = max(max_x, minmaxes[particle][4])
                        max_z = max(max_x, minmaxes[particle][5])
                    if min_x < 0:
                        min_x = 0
                    if min_y < 0:
                        min_y = 0
                    if min_z < 0:
                        min_z = 0
                    if max_x > edge_len:
                        max_x = edge_len
                    if max_y > edge_len:
                        max_y = edge_len
                    if max_z > edge_len:
                        max_z = edge_len
                    cluster['cluster_x_len'] = max_x - min_x
                    cluster['cluster_y_len'] = max_y - min_y
                    cluster['cluster_z_len'] = max_z - min_z
    return entries


def analyze_average_clusteriaztion_rate(clusters, filler_R, filler_h, N):
    clusterized_particles_number = 0
    clusters_number = len(clusters)
    for cluster in clusters:
        clusterized_particles_number += cluster['cluster_size']
    return clusterized_particles_number / N


def analyze_average_cluster_size(clusters):
    ave_cluster_size = 0  
    clusters_number = len(clusters)
    if clusters_number == 0:
        return 1
    for cluster in clusters:
        ave_cluster_size += cluster['cluster_size']
    ave_cluster_size /= clusters_number
    return ave_cluster_size


def analyze_average_cluster_length(clusters):
    if len(clusters) == 0:
        return 0
    cluster_size_sum_x = 0
    cluster_size_sum_y = 0
    cluster_size_sum_z = 0
    for cluster in clusters:
        cluster_size_sum_x += cluster['cluster_x_len']
        cluster_size_sum_y += cluster['cluster_y_len']
        cluster_size_sum_z += cluster['cluster_z_len']
    ave_len = (cluster_size_sum_x + cluster_size_sum_y + cluster_size_sum_z) / 3
    return ave_len / len(clusters)


if __name__ == '__main__':
    f = open('options.ini', 'r')
    for line in f:
        if line.startswith('THICKNESS'):
            h = float(line.split()[1])
        if line.startswith('SHELL_THICKNESS'):
            sh = float(line.split()[1])
        if line.startswith('CUBE_EDGE_LENGTH'):
            edge_len = float(line.split()[1])
        if line.startswith('OUTER_RADIUS'):
            filler_R = float(line.split()[1])
    f = open('1.geo', 'r')
    N = 0
    for line in f:
        if line.startswith('solid polygonalCylinder'):
            N += 1
    tau = str(sh / h)
    if tau == '5.0':
        tau = '5'
    clusters = get_clusters_from_files(tau, N, edge_len)
    rate = analyze_average_clusteriaztion_rate(clusters, filler_R, h, N)
    size = analyze_average_cluster_size(clusters, edge_len) # size in particles
    length = analyze_average_cluster_length(clusters)
