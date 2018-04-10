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
        f_py_log = open(results_folder +
                            '/py_logs/' + new_entry['structure_name'],
                        'r')
        line_in_py = f_py_log.readline().split(':')
        f_clusters = open(results_folder + '/clusters/' +
                              new_entry['structure_name'],
                          'r')
        clu_num = 0
        for line in f_clusters: 
            clu_num += 1
        new_entry['fi'] = float(line_in_cpp[1])
        new_entry['Nreal'] = int(line_in_cpp[3])
        new_entry['att_real'] = int(line_in_cpp[5])
        new_entry['clu_rate'] = float(line_in_py[1])
        new_entry['ave_clu_size'] = float(line_in_py[3])
        new_entry['ave_clu_len'] = float(line_in_py[5])
        new_entry['clusters_num'] = int(clu_num)
        list_of_entries.append(new_entry)
    return list_of_entries


def pretty_fprint_db(db, fname_db, sorted_keys):
    f = open(fname_db, 'w')
    for entry in db:
        str_out = ''
        for key in sorted_keys:
            str_out += str(key) + ':' + str(entry[key]) + ':'
        str_out = str_out[:-1] + '\n'
        f.write(str_out)
    f.close()


def main():
    if len(sys.argv) < 2:
        print('usage: ./db_creation reulst_folder')
        return None
    results_folder = sys.argv[1]
    list_of_entries = create_list_of_entries(results_folder)
    print(len(list_of_entries), 'entries')
    #"""
    # what values are already covered
    #
    keys = ['L', 'N', 'R', 'h', 'sh', 'tau']
    values = {key: set() for key in keys}
    for entry in list_of_entries:
        for key in keys:
            values[key].add(entry[key])
    for key in keys:
        align = ' ' * (4 - len(key))
        print(key, align, *sorted(list(values[key])))
    #
    #"""
    fname_db = 'db'
    sorted_keys = [
        'structure_name',                          # name of structure
        'L', 'N', 'R', 'h', 'sh', 'tau', 'tra',    # desired parameters
        'Nreal', 'att_real', 'fi',                 # real values of cpp parameters
        'ave_clu_len', 'ave_clu_size', 'clu_rate', # some properties of resulting
        'clusters_num'                             #   system
    ]
    pretty_fprint_db(list_of_entries, fname_db, sorted_keys)

main()
