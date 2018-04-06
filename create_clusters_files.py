#!/usr/bin/env python3


def create_clusters_files():
    """
    """
    Ns = [4, 8, 12, 16, 20, 24, 28, 30]
    taus = ['1.5', '2.5', '5']
    folder_intersection = 'intersections'
    #for tau in taus:
    #    for N in Ns:
    #        for attempt in range(5):
    if True:
        if True:
            if True:
                # open file with list of intersections in the system
                fname = 'intersections.log'
                fin = open(fname, 'r')
                # read intersections
                intersections = []
                for line in fin:
                    if len(line) > 1:
                        ls = line.split()
                        particle1 = int(ls[0])
                        particle2 = int(ls[1])
                        intersections.append([particle1, particle2])
                # create clusters from intersections
                clusters = []
                #for loop_number in range(N):
                if True:
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
                repeating_clusters = []
                for i, cluster_i in enumerate(clusters):
                    for j, cluster_j in enumerate(clusters):
                        if i == j:
                            continue
                        if len(cluster_i) != len(cluster_j):
                            continue
                        same_elements_number = 0
                        for particle in cluster_i:
                            if particle in cluster_j:
                                same_elements_number += 1
                        if same_elements_number == len(cluster_i):
                            if ((i not in repeating_clusters) and
                                (j not in repeating_clusters)):
                                    repeating_clusters.append(j)
                non_repeating_clusters = []
                for i in range(len(clusters)):
                    if i not in repeating_clusters:
                        clusters[i].sort()
                        non_repeating_clusters.append(clusters[i])
                fout = open('clusters', 'w')
                for cluster_num, cluster in enumerate(non_repeating_clusters):
                    str_out = ''
                    for particle_num, particle in enumerate(cluster):
                        str_out += str(particle)
                        if particle_num != len(cluster) - 1:
                            str_out += ' '
                    if cluster_num != len(non_repeating_clusters) - 1:
                        str_out += '\n'
                    fout.write(str_out)


if __name__ == '__main__':
    create_clusters_files()
