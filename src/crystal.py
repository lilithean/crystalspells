#!/usr/bin/env python
#
# Copyright (C) 2018 Xiaoyu Wang <xwang224@buffalo.edu>
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

import sys, os
from spells import *

class Crystal(object):

    def __init__(self):

        self.lattice = [[1., 0., 0.], 
                        [0., 1., 0.], 
                        [0., 0., 1.]]
        self.ion = []

    def from_file(self, fname, fmt='vasp'):

        fmt = fmt.lower()

        if fmt in ('vasp', 'poscar', 'contcar'):
            with open(fname, 'r') as fid:
                s = fid.readlines()
            scale = float(s[1])
            self.lattice = [[float(x)*scale for x in y.split()] for y in s[2:5]]
            ele_name = s[5].split()
            ele_num = [int(x) for x in s[6].split()]
            if s[8][0].lower() == 's': 
                k = 9
            else: 
                k = 8
            if s[7][0].lower() == 'd':
                for i in range(len(ele_name)):
                    for j in range(ele_num[i]):
                        self.ion.append([ele_name[i]]+[float(x)*scale for x in s[k].split()[:3]])
                        k += 1
            elif s[7][0].lower() == 'c':
                sys.exit(-1)

    def to(self, fname=False, typ='d', fmt='vasp'):

        fmt = fmt.lower()
        typ = typ.lower()
        output = ''

        if fmt in ('vasp', 'poscar', 'contcar'):
            ele_name = []
            ele_num = []
            pos_list = []
            for i in self.ion:
                if i[0] in ele_name:
                    j = ele_name.index(i[0])
                    ele_num[j] += 1
                    pos_list[j].append(i[1:])
                else:
                    ele_name.append(i[0])
                    ele_num.append(1)
                    pos_list.append([i[1:]])
            title = ''.join(['%s%s' % (ele_name[x], ele_num[x]) for x in range(len(ele_name))])
            output += title + '\n'
            output += '1.0000000\n'
            output += ''.join(['%12.7f   %12.7f   %12.7f\n' % (x[0], x[1], x[2]) for x in self.lattice])
            output += '  '.join(ele_name) + '\n'
            output += '  '.join([str(x) for x in ele_num]) + '\n'
            if typ[0] == 'c' or typ[0] == 'k':
                output += 'cartesian\n'
                output += '\n'.join(['   '.join(['%12.7f' % z for z in self.cartesian(y)]) for x in pos_list for y in x])   
            else:
                output += 'direct\n'
                output += '\n'.join(['%12.7f   %12.7f   %12.7f' % (x[0], x[1], x[2]) for y in pos_list for x in y])   

        if not fname:
            print output
        else:
            with open(fname, 'w') as fid:
                fid.write(output)

    def copy(self):
        k = Crystal()
        k.lattice = self.lattice
        k.ion = self.ion
        return k

    def cartesian(self, pos):
        return [self.lattice[0][0] * pos[0] + self.lattice[1][0] * pos[1] + self.lattice[2][0] * pos[2],
                self.lattice[0][1] * pos[0] + self.lattice[1][1] * pos[1] + self.lattice[2][1] * pos[2],
                self.lattice[0][2] * pos[0] + self.lattice[1][2] * pos[1] + self.lattice[2][2] * pos[2]]

    def distance(self, i, j):
        ab_frac = [self.ion[i][x] - self.ion[j][x] for x in range(1, 4)]
        sgn = [1. + -2.*float(x < 0) for x in ab_frac]
        ab = [self.cartesian(ab_frac)] # 0: A->B
        ab.append([ab[0][0] - self.lattice[0][0]*sgn[0], ab[0][1] - self.lattice[0][1]*sgn[0], ab[0][2] - self.lattice[0][2]*sgn[0]]) # 1: A+a->B
        ab.append([ab[0][0] - self.lattice[1][0]*sgn[1], ab[0][1] - self.lattice[1][1]*sgn[1], ab[0][2] - self.lattice[1][2]*sgn[1]]) # 2: A+b->B
        ab.append([ab[0][0] - self.lattice[2][0]*sgn[2], ab[0][1] - self.lattice[2][1]*sgn[2], ab[0][2] - self.lattice[2][2]*sgn[2]]) # 3: A+c->B
        ab.append([ab[1][0] - self.lattice[1][0]*sgn[1], ab[1][1] - self.lattice[1][1]*sgn[1], ab[1][2] - self.lattice[1][2]*sgn[1]]) # 4: A+a+b->B
        ab.append([ab[1][0] - self.lattice[2][0]*sgn[2], ab[1][1] - self.lattice[2][1]*sgn[2], ab[1][2] - self.lattice[2][2]*sgn[2]]) # 5: A+a+c->B
        ab.append([ab[2][0] - self.lattice[2][0]*sgn[2], ab[2][1] - self.lattice[2][1]*sgn[2], ab[2][2] - self.lattice[2][2]*sgn[2]]) # 6: A+b+c->B
        ab.append([ab[4][0] - self.lattice[2][0]*sgn[2], ab[4][1] - self.lattice[2][1]*sgn[2], ab[4][2] - self.lattice[2][2]*sgn[2]]) # 7: A+a+b+c->B
        return min([(x[0]**2. + x[1]**2. + x[2]**2.)**.5 for x in ab])

    def adjacent_matrix(self, r_min=0., r_max=1.8):
        n = len(self.ion)
        adj_mat = [[0]*n for i in range(n)]
        for i in range(n):
            for j in range(1+i, n): 
                 if r_min <= self.distance(i, j) <= r_max:
                      adj_mat[i][j] = adj_mat[j][i] = 1
        return adj_mat         
             
    def super_cell(self, scale=[2, 2, 2]):
        k = self.copy()
        k.lattice = [[self.lattice[y][x] * scale[y] for x in range(3)] for y in range(3)]
        k.ion = [[x[0], (x[1]+u)/scale[0], (x[2]+v)/scale[1], (x[3]+w)/scale[2]] for x in self.ion for u in range(scale[0]) for v in range(scale[1]) for w in range(scale[2])] 
        return k

    def reciprocal_lattice(self, two_pi=False):
        # In vasp 2pi is in the wave vector
        # b1 = (a2_a3)/(a1 (a2_a3))
        # b2 =  a3_a1   a2  a3_a1
        # b3 =  a1_a2   a3  a1_a2
        numerator = [cross_prod(self.lattice[1], self.lattice[2]), cross_prod(self.lattice[2], self.lattice[0]), cross_prod(self.lattice[0], self.lattice[1])]
        denominator = [dot_prod(self.lattice[x], numerator[x]) for x in range(3)]
        return [[numerator[x][y]/denominator[x] for y in range(3)] for x in range(3)]

    def k_mesh(self, n_per_distance=50, odd=True):
        recip_len = [(x[0]**2 + x[1]**2 + x[2]**2)**.5 for x in self.reciprocal_lattice()]
        kpts_vasp = [round(max([1., n_per_distance*recip_len[x]])) for x in range(3)]
        kpts_total = kpts_vasp[0]*kpts_vasp[1]*kpts_vasp[2]
        #max_kpts = max(kpts_vasp)
        #which_lat = kpts_vasp.index(max_kpts)
        ratio = [1/sum([self.lattice[x][y]**2 for y in range(3)])**0.5 for x in range(3)]  
        s = (kpts_total/ratio[0]/ratio[1]/ratio[2])**0.333333333333
        k_mesh = [-(-s*ratio[x] // 1) for x in range(3)]
        if odd:
            k_mesh = [k_mesh[x] + (not (k_mesh[x] % 2)) for x in range(3)]
        return k_mesh
