#!/usr/bin/env python3


import math
import os
import pprint
pprint=pprint.PrettyPrinter(indent=4).pprint
import random
import subprocess


test_results_folder = 'results_new'


# Abbreviations:
#
# d - distance
# N - number for particles
# n - number for chains
# per - percolated
# irreg - irregular
# ps - Polygonal Sphere


class PolygonalSphere:
    def __init__(self, cx, cy, cz, r, N=20):
        self.cx = cx
        self.cy = cy
        self.cz = cz
        self.r = r
        self.N = N

    def geo_str(self, name):
        str_out = 'solid {0} =\n'.format(name)
        alphas = [i * 2 * math.pi / self.N for i in range(self.N)]
        betas = [i * 2 * math.pi / self.N for i in range(self.N)]
        for alpha in alphas:
            for beta in betas:
                x = self.cx + self.r * math.cos(alpha) * math.cos(beta)
                y = self.cy + self.r * math.sin(alpha) * math.cos(beta)
                z = self.cz + self.r * math.sin(beta)
                factor = 1. / math.cos(2 * math.pi / self.N)**2
                nx = self.r * math.cos(alpha) * math.cos(beta)
                ny = self.r * math.sin(alpha) * math.cos(beta)
                nz = self.r * math.sin(beta)
                str_out += '\tplane({0}, {1}, {2}; {3}, {4}, {5})'.format(x, y, z,
                               nx, ny, nz)
                str_out += '\n\tand\n'
        str_out = str_out[:-5] + ';\n'
        return str_out


def out_geo(system, fname, N=5):
    str_out = 'algebraic3d\n\n'
    str_fil = 'solid filler =\n'
    str_int = 'solid interface =\n'
    str_mat = 'solid matrix =\n\t'
    pss = system['particles']
    r = system['r']
    sh = system['sh']
    L = system['L']
    str_brick = 'orthobrick('
    str_brick += '{0}, {1}, {2}; {3}, {4}, {5})'.format(0, 0, 0, L, L, L)
    for i in range(len(pss)):
        if i != 0:
            str_mat += '\n\tand '
        ps_fil = PolygonalSphere(pss[i][0], pss[i][1], pss[i][2], r, N)
        ps_int = PolygonalSphere(pss[i][0], pss[i][1], pss[i][2], r + sh, N)
        str_fil_ps = ps_fil.geo_str('filler' + str(i))
        str_int_ps = ps_int.geo_str('shell' + str(i))
        str_int_util_ps = ps_int.geo_str('shell_util' + str(i))
        str_out += str_fil_ps[:-2] + '\tand\n\t' + str_brick + '\n;\n'
        str_out += str_int_ps[:-2] + '\tand\n\t' + str_brick + '\n;\n'
        str_out += str_int_util_ps[:-2] + '\nand\n\t' + str_brick + '\n;\n'
        str_fil += '\tfiller' + str(i)
        str_int += '\t(shell' + str(i) + ' and not filler' + str(i)  + ')'
        str_mat += 'not\n\tshell_util' + str(i)
        if i != len(pss) - 1:
            str_fil += '\n\tor\n'
            str_int += '\n\tor\n'
    str_fil += '\n;\n'
    str_int += '\n;\n'
    str_mat += '\n\tand\n\t' + str_brick + '\n ;'
    str_out += str_fil + str_int + str_mat
    str_out += '\ntlo filler;'
    str_out += '\ntlo interface -transparent;'
    str_out += '\ntlo matrix -transparent;'
    f = open(fname, 'w')
    f.write(str_out)
    return None


def make_systems(r, sh, overlap, n_chains, max_attempts=10, scaling=1.):
  # per
    # Minimal distance between centers of non-intersecting
    # particles
    d_bw_c = 2 * (r + sh) * scaling
    n_chains_1d = n_chains**0.5
    if not n_chains_1d.is_integer():
        print('inconsistent number of chains')
        return None
    # Minimal length of cubic cell in directions that are transverse
    # to chains directions when there are n_chains_1d chains in
    # directions of every axes.
    if n_chains_1d > 1:
        L_transverse_min = (n_chains_1d - 1) * d_bw_c + 2 * (r + sh)
    else:
        L_transverse_min = 2 * (r + sh)
    tmp = L_transverse_min + sh * overlap
    tmp += 4 * (r + sh * (1 - overlap))
    tmp -= 2 * (r + sh * (2 - overlap))
    tmp /= overlap * sh + 2 * (r + sh * (1 - overlap))
    # If longitudal length equals transversal length, every chain
    # contains this number of particles.
    if tmp.is_integer():
        N_in_chain = tmp
    else:
        N_in_chain = int(tmp) + 1
    N_in_chain = int(max(2, N_in_chain))
    tmp = (N_in_chain - 1) * overlap * sh
    tmp += (N_in_chain - 2) * (2 * r + 2 * (1 - overlap) * sh)
    tmp += 2 * (2 * r + sh * (2 - overlap))
    # Length of box that leads to the case when chain with N_in_chain
    # particles spans from one side to the oppoiste.
    L_longitudal = tmp
    # If chains are long and longitudal distance is greater than
    # transverse distance, we should extend the distance between chains.
    if n_chains_1d > 1:
        if L_longitudal > L_transverse_min:
            d_bw_c += (L_longitudal - L_transverse_min) / (n_chains_1d - 1)
            L_transverse = (n_chains_1d - 1) * d_bw_c + 2 * (r + sh)
        else:
            # Chains are too short, we should add particles to them.
            while L_longitudal < L_transverse_min:
                N_in_chain += 1
                L_longitudal += overlap * sh + (2 * r + 2 * (1 - overlap) * sh)
    else:
        if L_longitudal > L_transverse_min:
            x = r + sh + (L_longitudal - L_transverse_min) / 2
            y = r + sh + (L_longitudal - L_transverse_min) / 2
            L_transverse = 2 * x
        else:
            while L_longitudal < L_transverse_min:
                N_in_chain += 1
                L_longitudal += overlap * sh + (2 * r + 2 * (1 - overlap) * sh)
    if abs(L_longitudal - L_transverse) / (L_transverse + L_longitudal) > 0.01:
        print('something gone wrong')
        return None
    n_chains_1d = int(n_chains_1d)
    particles_per = []
    if n_chains_1d > 1:
        for i in range(n_chains_1d):
            x = sh + r
            if i > 0:
                x += d_bw_c * i
            for j in range(n_chains_1d):
                y = sh + r
                if j > 0:
                    y += d_bw_c * j
                for k in range(N_in_chain):
                    z = r + sh
                    if k > 0:
                        z += k * (2 * r + sh + sh * (1 - overlap))
                    particles_per.append([x, y, z])
    else:
        for k in range(N_in_chain):
             z = r + sh
             if k > 0:
                 z += k * (2 * r + sh + sh * (1 - overlap))
             particles_per.append([x, y, z])
    system_per = {
        'r': r,
        'sh': sh,
        'L': L_longitudal,
        'particles': particles_per
    }
  # irreg
    particles_irreg = []
    r_sqr = r**2
    attempts = 0
    while n_chains_1d**2 * N_in_chain > len(particles_irreg):
        if attempts == max_attempts:
            print('maximum attempts number achieved')
            print(len(particles_irreg), '/', n_chains_1d**2 * N_in_chain, 'done')
            break
        attempts += 1
        x = sh + r + random.random() * (L_longitudal - 2 * r - 2 * sh)
        z = sh + r + random.random() * (L_longitudal - 2 * r - 2 * sh)
        y = sh + r + random.random() * (L_longitudal - 2 * r - 2 * sh)
        flag = False # becomes true if particle intersects with other
        for particle in particles_irreg:
            dx = particle[0] - x
            dy = particle[1] - y
            dz = particle[2] - z
            if dx**2 + dy**2 + dz**2 < 2 * r_sqr:
                flag = True
                break
        if not flag:
            particles_irreg.append([x, y, z])
    if n_chains_1d**2 * N_in_chain == len(particles_irreg):
        system_irreg = {
            'r': r,
            'sh': sh,
            'L': L_longitudal,
            'particles': particles_irreg,
            'attempts': attempts
        }
    else:
        system_irreg = None
    return [system_per, system_irreg]


def run_one_time(test_results_folder,
                 r, sh, double_overlap, n_chains, max_attempts, scaling):
    [system_per, system_irreg] = make_systems(r, sh, double_overlap, n_chains,
                                              max_attempts, scaling)
    if None in [system_per, system_irreg]:
        log_str = 'error in run_one_time:' + ' at least one system is not made'
    else:
        N = float(len(system_irreg['particles']))
        L = float(system_irreg['L'])
        attempts = system_irreg['attempts']
        fi = math.pi * 4 / 3 * r**3 * N / L**3
        tau = sh / r
        log_str = ' '.join(['success',
                            'tau', str(tau), 'filler_fi', str(fi), 'N',
                            str(int(N)), 'L', str(L), 'attempts',
                            str(attempts)])
        structure_fname = ('n_' + str(n_chains) + '_tau_' + str(tau) + '_fi_' +
                           str(fi) + '.geo')
        fname_per = test_results_folder + '/geo/per/' + structure_fname
        fname_irreg = test_results_folder + '/geo/irreg/' + structure_fname
        out_geo(system_per, fname_per)
        out_geo(system_irreg, fname_irreg)
    return log_str


def main(test_results_folder='results'):
    """
    This script is designed to make 2 structures
        - irregular system of non-interacting spheres
        - system of interacting spheres
    and to compare them in order to study the influence of
    geometrical percolation on the mechanical properties.
    """
    # pre-run
    # subprocess.call(['rm', '-rf', test_results_folder])
    if test_results_folder in os.listdir():
        print('test_results_folder folder exists')
        return None
    subprocess.call(['mkdir', test_results_folder])
    subprocess.call(['mkdir', test_results_folder + '/geo'])
    subprocess.call(['mkdir', test_results_folder + '/geo/irreg'])
    subprocess.call(['mkdir', test_results_folder + '/geo/per'])
    log = open(test_results_folder + '/create_systems2_log', 'w')
    r = 1.
    sh = 1.
    double_overlap = 1 # multiplied by 2 united part of interface thiskness
    max_attempts = 10000 # maximum attempts number to create irregular system
    #ns_chains = [1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144, 169,
    #             196, 225]
    #scaling = 7.5

    n_chains = 4
    scaling = 1
    fi = 1 # start value
    min_fi_filler = 0.001


    while fi > min_fi_filler:
        log_str = run_one_time(test_results_folder, r, sh, double_overlap,
                               n_chains, max_attempts, scaling)
        fi = float(log_str.split()[4])
        log.write(log_str)
        scaling *= 1.05
    return None


if __name__ == '__main__':
    main()
