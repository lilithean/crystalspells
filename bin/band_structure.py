#!/usr/bin/env python
#
# Copyright (C) 2019 Xiaoyu Wang <xwang224@buffalo.edu>
#
# This file is part of CrystalSpells Package
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# instruction:
# A. First you should have the following files in the folder:
# 1. POSCAR:
#   Will read the lattice parameters. Also the KPOINTS file will be taken 
# to calculate the distance in the reciprocal space.
#
# 2. EIGENVAL: 
#   Will read eigenvalues from the band-structure calculation.
#
# 3. DOSCAR: 
#   Will read density of states from the mesh grid calculation. 
#   Also read fermi level, and all energies will be shifted. 
#   Can use a band-structure calculation DOSCAR instead
#
# 4. KPOINTS: 
#   k-path for the band-structure calculation. 
#   The last word at each line will be taken as the label. 
#   If not present a '^' will present to point the position.
#
# B. Parameters might can be set:
dos = False    # plot density of states?
energy_above_fermi = 12
energy_below_fermi = 15
silence = True    # output data to stdout, then you can pip it into a file 
plot_show = False
plot_write = True

import sys
sys.path.append('/projects/academic/ezurek/xiaoyu/src/crystalspells/src/')
import numpy as np
from crystal import *
import matplotlib.pyplot as plt

# read eigenvalues from eigenval
with open('EIGENVAL', 'r') as fid:
    data = fid.readlines()
n_elec, n_kpts, n_bnd = (int(x) for x in data[5].split())
kpoints = [[float(x) for x in y.split()[:3]] for y in data[7::n_bnd+2]]

# read structure from poscar
A = Crystal()
A.from_file('POSCAR')

# create a lattice contians reciprocal information
B = Crystal()
B.lattice = A.reciprocal_lattice()

# read k-path from kpoints
with open('KPOINTS', 'r') as fid:
    kpt_data = fid.readlines()
    kpt_data = [x for x in kpt_data if len(x.split()) > 0]
    # please note that this will read the first three numbers as k-point, 
    # and the last word as label if len(x) > 3
    n_dot = int(kpt_data[1].split()[0])
    kpt_format = kpt_data[3][0].upper()
    if kpt_format == 'R':
        B.ion = [[y.split()[-1] if len(y.split()) > 3 else '^'] 
                + [float(x) for x in y.split()[:3]] for y in kpt_data[4:]]
    elif kpt_format == 'C' or kpt_format == 'K':
        print "currently the cartesian kpts has not been employed"
        sys.exit(-1)

# read fermi-level and dos from doscar 
with open('DOSCAR', 'r') as fid:
    dos_data = fid.readlines()
    e_fermi = float(dos_data[5].split()[3])
 
# calculate the k-path connectivity
X = [0.]
X_ends = [0]
X_ticks = [0]
X_label = [r'$%s$' % B.ion[0][0]]
for i in range(1, len(B.ion), 2):
    frac_vec = [B.ion[i][x] - B.ion[i-1][x] for x in range(1, 4)]
    cart_dist = np.linalg.norm(B.cartesian(frac_vec))
    X += [X[-1] + cart_dist*x/float(n_dot) for x in range(1, n_dot+1)]
    X_ticks.append(int((i+1)*n_dot*0.5))
    if i == len(B.ion)-1:
        X_label.append(r'$%s$' % B.ion[i][0])
        X_ends.append(X_ticks[-1])
    elif B.ion[i][0] == B.ion[i+1][0]:
        X_label.append(r'$%s$' % B.ion[i][0])
    else:
        X_label.append(r"$%s|%s$" % (B.ion[i][0], B.ion[i+1][0]))
        X_ends.append(X_ticks[-1])
for i in range(1, len(X_ends)):
    X_ticks = [x if x <= X_ends[i]-i else x-1 for x in X_ticks]

# assign eigenvalues to each band
Y = [[float(x[5:20:1])-e_fermi for x in data[8:8+n_bnd:1]]]
for i in range(1, n_kpts):
    Y.append([float(x[5:22:1])-e_fermi 
              for x in data[8+i*(n_bnd+2):8+i*(n_bnd+2)+n_bnd:1]]) 
Y_T = map(list, zip(*Y))

# generate a matplotlib plot
for i in range(n_bnd):
    if -15 <= Y_T[i][0] <= 10:
        for j in range(1, len(X_ends)):
            plt.plot(X[X_ends[j-1]+1-j:X_ends[j]+1-j], 
                     Y_T[i][X_ends[j-1]:X_ends[j]], 
                     c='k',
                     lw=0.5)

for i in X_ticks[1:-1]:
    plt.plot([X[i], X[i]], 
             [-20, 20], 
             c='#d3d3d3',
             lw=0.7)
plt.xlim(X[1], max(X[:-len(X_ends)+1]))
plt.ylim(-13, 12)
plt.tick_params(direction='in', 
                axis='both',
                bottom=True, top=True, left=True, right=True)
plt.xticks([X[x] for x in X_ticks], X_label)
plt.xlabel("cartesian distance in reciprocal space")
plt.ylabel(r"E - E$_f$ (eV)")
if plot_show:
    plt.show()
if plot_write:
    plt.savefig(sys.argv[1])

# output data to stdout
if not silence:
    for i in range(n_kpts):
        print ' %2.6f ' % X[i], '  ' + '  '.join(['%2.6f' %x for x in Y[i]])
