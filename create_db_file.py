#!/usr/bin/env python3


import sys

import pprint
pprint=pprint.PrettyPrinter(indent=4).pprint


def create_list_of_entries(results_folder):
    list_of_entries = []
    f_structures_log = open(results_folder + '/structures_log', 'r')
    for line in f_structures_log:
        new_entry = {}
        for i in range(int(len(line.split(':')) / 2)):
            key = line.split(':')[2 * i]
            value = line.split(':')[2 * i + 1]
            try:
                value = int(value)
            except:
                try:
                    value = float(value)
                except:
                    pass
            new_entry[key] = value
        f_cpp_output = open(results_folder + '/logs_cpppolygons/' +
                                new_entry['structure_name'],
                            'r')
        line_in_cpp = f_cpp_output.readline().split(':')
        f_clusters = open(results_folder + '/clusters/' +
                              new_entry['structure_name'],
                          'r')
        f_cluster_lengths = open(results_folder + '/clusters_lengths/' +
                                     new_entry['structure_name'],
                                 'r')
        line_in_clu_lengths = f_cluster_lengths.readline().split()
        clu_num = 0
        clusterized = 0.0
        for line in f_clusters: 
            clusterized += len(line.split())
            clu_num += 1
        new_entry['fi'] = float(line_in_cpp[1])
        new_entry['Nreal'] = int(line_in_cpp[3])
        new_entry['att_real'] = int(line_in_cpp[5])
        new_entry['clusters_num'] = int(clu_num)
        new_entry['clusterization_rate'] = clusterized / float(new_entry['Nreal'])
        if clu_num > 0:
            new_entry['ave_cluster_size'] = clusterized / float(clu_num)
            new_entry['ave_cluster_x_len'] = float(line_in_clu_lengths[0])
            new_entry['ave_cluster_y_len'] = float(line_in_clu_lengths[1])
            new_entry['ave_cluster_z_len'] = float(line_in_clu_lengths[2])
            new_entry['ave_cluster_len'] = float(line_in_clu_lengths[3])
        else:
            new_entry['ave_cluster_size'] = None
            new_entry['ave_cluster_x_len'] = None
            new_entry['ave_cluster_y_len'] = None
            new_entry['ave_cluster_z_len'] = None
            new_entry['ave_cluster_len'] = None
        list_of_entries.append(new_entry)
    return list_of_entries


def pretty_fprint_db(db, fname_db, sorted_keys):
    f = open(fname_db, 'w')
    for entry in db:
        str_out = ''
        for key in sorted_keys:
            if key not in entry.keys():
                 print(key) 
                 continue
            str_out += str(key) + ':' + str(entry[key]) + ':'
        str_out = str_out[:-1] + '\n'
        f.write(str_out)
    f.close()


def create_db_file():
    """
    After all systems are prepared and all parameter are calculated,
    one can create a database.
    """
    # configuring
    results_folder = 'results'
    fname_db = 'system_db' 
    list_of_entries = create_list_of_entries(results_folder)
    #
    # discover what values are already covered
    #
    sorted_keys = [
        'structure_name',                          # name of structure
        'L', 'N', 'R', 'h', 'sh', 'tau', 'tra',    # desired parameters
        'Nreal', 'att_real', 'fi',                 # real values of cpp parameters
        'ave_cluster_size',                        # clusters properties
        'clusters_num', 'clusterization_rate',
        'ave_cluster_x_len', 'ave_cluster_y_len', 'ave_cluster_z_len',
        'ave_cluster_len'
    ]
    pretty_fprint_db(list_of_entries, fname_db, sorted_keys)


if __name__ == '__main__':
    create_db_file()
