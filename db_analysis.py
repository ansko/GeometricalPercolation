#!/usr/bin/env python3


import pprint
pprint=pprint.PrettyPrinter(indent=4).pprint



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

def plot1():
    """
    Clusterization rate vs fi.
    """
    db = get_db()
    pass
    print('end')
    return None


plot1()

"""
all_keys = [
    'structure_name',
    'L', 'N', 'R', 'h', 'sh', 'tau', 'tra',
    'Nreal', 'att_real', 'fi',
    'ave_clu_len', 'ave_clu_size', 'clu_rate'
]
"""
