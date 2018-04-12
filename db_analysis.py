#!/usr/bin/env python3


import os

import pprint
pprint=pprint.PrettyPrinter(indent=4).pprint


log_folder = 'logs100k'

#
# May be a bad idea!
#
# fi values when Nreal == Ndesired
full_fis = set((
    0.00942478,
    0.0188496,
    0.0282743,
    0.0376991,
    0.0471239,
    0.0565487,
    0.0659735
))
taus = [1.5, 2.5, 5.0]


def get_db(db_fname='system_db'):
    db = []
    f = open(db_fname, 'r')
    for line in f:
        entry = {}
        ls = line[:-1].split(':')
        for i in range(int(len(ls) / 2)):
            key = ls[2 * i]
            value = ls[2 * i + 1]
            try:
                value = int(value)
            except:
                try:
                    value = float(value)
                except:
                    value = str(value)
                if value == 'None':
                    value = None
            entry[key] = value
        db.append(entry)
    return db


def N_div_fi_div_L3_L():
    Ls = set()
    Ns = set()
    db = get_db()
    for entry in db:
        Ls.add(int(entry['L']))
        Ns.add(int(entry['Nreal']))
    Ls = sorted(list(Ls))
    Ns = sorted(list(Ns))
    result = { L: { N: [] for N in Ns} for L in Ls }
    result_ave = { L: [] for L in Ls }
    for entry in db:
        fi = float(entry['fi'])
        L = int(entry['L'])
        N = int(entry['Nreal'])
        result[L][N].append(float(N) / fi / float(L**3))     # should be const
        result_ave[L].append(float(N) / fi / float(L**3))    # -||-
    for L in Ls:
        if result_ave:
            result_ave[L] = float(sum(result_ave[L])) / float(len(result_ave[L]))
        else:
            result_ave[L] = None
        for N in Ns:
            if result[L][N]:
                result[L][N] = float(sum(result[L][N])) / float(len(result[L][N]))
            else:
                result[L][N] = None
    f = open(log_folder + '/ave_N_div_fi_div_L3_on_L', 'w')
    f.write('L ave(L/(fi*N)) averaged_over_this_N\n')
    for L in Ls:
        if result_ave is not None:
            f.write(' '.join([str(L), str(result_ave[L])]) + '\n')


def clu_rate_vs_fi_on_tau():
    db = get_db()
    taus = set()
    fis = set()
    for entry in db:
        fis.add(float(entry['fi']))
        taus.add(float(entry['tau']))
    taus = sorted(list(taus))
    fis = sorted(list(fis))
    result = { tau: { fi: [] for fi in fis } for tau in taus }
    for entry in db:
        fi = float(entry['fi'])
        tau = float(entry['tau'])
        rate = float(entry['clusterization_rate'])
        result[tau][fi].append(rate)
    for tau in taus:
        f = open(log_folder + '/clu_rate_vs_fi_on_tau_' + str(tau), 'w')
        f.write('fi ave(clu_rate) averaged_over_this_N\n')
        for fi in fis:
            f.write(' '.join([str(fi),
                              str(sum(result[tau][fi]) / len(result[tau][fi])),
                              str(len(result[tau][fi])),
                              '\n']))


def clu_len_vs_fi_on_tau():
    db = get_db()
    taus = set()
    fis = set()
    for entry in db:
        fis.add(float(entry['fi']))
        taus.add(float(entry['tau']))
    taus = sorted(list(taus))
    fis = sorted(list(fis))
    result = { tau: { fi: [] for fi in fis } for tau in taus }
    for entry in db:
        fi = float(entry['fi'])
        L = float(entry['L'])
        tau = float(entry['tau'])
        length = entry['ave_cluster_len']
        try:
            result[tau][fi].append(float(length) / L)
        except:
            pass
    for tau in taus:
        f = open(log_folder + '/clu_len_vs_fi_on_tau_' + str(tau), 'w')
        f.write('fi ave(cluster_len/N) averaged_over_this_N\n')
        for fi in fis:
            if not result[tau][fi]:
                continue
            f.write(' '.join([str(fi),
                              str(sum(result[tau][fi]) / len(result[tau][fi])),
                              str(len(result[tau][fi])),
                              '\n']))

def full_analysis():
    clu_len_vs_fi_on_tau() # clusterization_rate vs. fi
    clu_rate_vs_fi_on_tau()            # average cluater length vs. fi
    N_div_fi_div_L3_L()     # should grow due to desrease of the depleted layer


if __name__ == '__main__':
    full_analysis()


"""
Keep this list up-to-date with the list from create_db_file.py

    sorted_keys = [
        'structure_name',                          # name of structure
        'L', 'N', 'R', 'h', 'sh', 'tau', 'tra',    # desired parameters
        'Nreal', 'att_real', 'fi',                 # real values of cpp parameters
        'ave_cluster_size',                        # clusters properties
        'clusters_num', 'clusterization_rate',
        'ave_cluster_x_len', 'ave_cluster_y_len', 'ave_cluster_z_len',
        'ave_cluster_len'
    ]
"""
