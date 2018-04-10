#!/usr/bin/env python3


import os

import pprint
pprint=pprint.PrettyPrinter(indent=4).pprint


results_folder = 'results100k'


def project(db, projection_keys):
    result = []
    for entry in db:
        new_entry = {}
        for key in projection_keys:
            new_entry[key] = entry[key]
        result.append(new_entry)
    return result


def average(db, keys):
    key_x = keys[0]
    key_x_values = set()
    key_y = keys[1]
    for entry in db:
        key_x_values.add(entry[key_x])
    key_x_values = list(key_x_values)
    key_x_values.sort()
    key_y_values = {
        key: [0, 0] for key in key_x_values
    }                                        # [sum, num] for every key_x
    for entry in db:
        key_y_values[entry[key_x]][0] += entry[key_y]
        key_y_values[entry[key_x]][1] += 1
    for key in key_y_values.keys():
        key_y_values[key] = float(key_y_values[key][0]) / key_y_values[key][1]
    return key_y_values


def get_db():
    db = []
    db_fname = 'db'
    f = open(db_fname, 'r')
    for line in f:
        entry = {}
        ls = line.split(':')
        for i in range(int(len(ls) / 2)):
            key = ls[2 * i]
            value = ls[2 * i + 1]
            try:
                value = int(value)
            except:
                try:
                    value = float(value)
                except:
                    pass
            entry[key] = value
        db.append(entry)
    return db


def intersections_to_clusters2(clusters):
    a = set()
    print(a)
    if a:
        print(a)
    return
    new_clusters = clusters

    cluster = new_clusters[0]
    for i in range(1, len(new_clusters)):
        for j in range(len(cluster)):
            if cluster[j] in new_clusters[i]:
                new_clusters[i] = set(new_clusters[i])
                new_clusters[i].update(cluster)
                print(i, j ,new_clusters[i])
                new_clusters[i] = list(new_clusters[i])
    new_clusters = [new_clusters[i] for i in range(1, len(new_clusters))]

    pprint(new_clusters)     
    return

def intersections_to_clusters(intersections):
    clusters = []
    # create clusters from intersections
    for intersection in intersections:
        particle1 = intersection[0]
        particle2 = intersection[1]
        flag_particle1_in_any_cluster = False
        clusters_with_particle1 = []
        flag_particle2_in_any_cluster = False
        clusters_with_particle2 = []
        for cluster_number, cluster in enumerate(clusters):
            if particle1 in  cluster:
                flag_particle1_in_any_cluster = True
                clusters_with_particle1.append(cluster_number)
            if particle2 in cluster:
                flag_particle2_in_any_cluster = True
                clusters_with_particle2.append(cluster_number)
        if ((not flag_particle1_in_any_cluster) and
            (not flag_particle2_in_any_cluster)):
                new_cluster = [particle1, particle2]
                clusters.append(new_cluster)
        else:
            if flag_particle1_in_any_cluster:
                for cluster_number in clusters_with_particle1:
                    if not particle2 in clusters[cluster_number]:
                        clusters[cluster_number].append(particle2)
            if flag_particle2_in_any_cluster:
                for cluster_number in clusters_with_particle2:
                    if not particle1 in clusters[cluster_number]:
                        clusters[cluster_number].append(particle1)
    # remove repeating clusters
    for _ in range(len(clusters)):
        if len(clusters) == 1:
            break
        repeating_clusters = []
        for i, cluster_i in enumerate(clusters):
            for j, cluster_j in enumerate(clusters):
                if i == j:
                   continue
                for particle in cluster_i:
                   if particle in cluster_j:
                       if len(cluster_j) > len(cluster_i):
                           repeating_clusters.append(i)
                       elif len(cluster_j) < len(cluster_i):
                           repeating_clusters.append(j)
                       else:
                           if (i not in repeating_clusters and
                               j not in repeating_clusters):
                                   repeating_clusters.append(i)
        clusters = [
            clusters[i] for i in (set(range(len(clusters))) -
                                  set(repeating_clusters))
            ]
    return clusters


def rate_fi():
    """
    Clusterization rate vs fi.
    """
    full_fis = set((
        0.00942478,
        0.0188496,
        0.0282743,
        0.0376991,
        0.0471239,
        0.0565487,
        0.0659735))
    taus = [1.5, 2.5, 5.0]
    db = get_db()
    tau_vals = set()
    result = {
        tau: {
            fi: [] for fi in full_fis
        } for tau in taus
    }
    for entry in db:
        structure_name = entry['structure_name']
        N = entry['Nreal']
        fi = entry['fi']
        if fi not in full_fis:
            continue
        tau = entry['tau']
        clusterized = 0
        f = open(results_folder + '/new_clusters/' + structure_name, 'r')
        for line in f:
            clusterized += len(line.split())
        result[tau][fi].append(clusterized / N)
    for tau in sorted(taus):
        f = open('logs/clu_rate_on_fi_' + str(tau), 'w')
        for fi in sorted(full_fis):
            if result[tau][fi]:
                f.write(
                    str(fi) +
                    ' ' +
                    '%.2f' % (sum(result[tau][fi]) / len(result[tau][fi])) +
                    ' ' +
                    str(len(result[tau][fi])) +
                    '\n')
            else:
                f.write(str(fi) + ' 0 0\n')
    return None


def clu_len_fi():
    """
    Clu_len / Box_len vs fi.
    """
    full_fis = set((
        0.00942478,
        0.0188496,
        0.0282743,
        0.0376991,
        0.0471239,
        0.0565487,
        0.0659735))
    taus = [1.5, 2.5, 5.0]
    db = get_db()
    Ls = set()
    for entry in db:
        Ls.add(entry['L'])
    Ls = sorted(list(Ls))
    result = {
       fi: {
           tau: [
           ] for tau in taus
       } for fi in full_fis
    }
    for entry in db:
        structure_name = entry['structure_name']
        fi = entry['fi']
        tau = entry['tau']
        L = entry['L']
        if fi not in full_fis:
            continue
        f = open(results_folder + '/new_clusters_lengths/' + structure_name, 'r')
        for line in f:
            result[fi][tau].append(float(line.split()[3]) / L)
    for fi in full_fis:
        for tau in taus:
            if result[fi][tau]:
                result[fi][tau] = sum(result[fi][tau]) / len(result[fi][tau])
            else:
                result[fi][tau] = 0
    for tau in taus:
        f = open('logs/clu_len_on_fi_' + str(tau), 'w')
        for fi in sorted(list(full_fis)):
            if result[fi][tau] is not None:
                f.write(' '.join([str(fi), str(result[fi][tau])]) + '\n')


rate_fi()  # clusterization_rate vs fi
clu_len_fi()


"""
all_keys = [
    'structure_name',
    'L', 'N', 'R', 'h', 'sh', 'tau', 'tra',
    'Nreal', 'att_real', 'fi',
    'ave_clu_len', 'ave_clu_size', 'clu_rate'
]
"""
