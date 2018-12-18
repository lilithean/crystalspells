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
        ab = [self.cartesian([self.ion[i][x] - self.ion[j][x] for x in range(1, 4)])] # 0: A->B
        ab.append([ab[0][0] - self.lattice[0][0], ab[0][1] - self.lattice[0][1], ab[0][2] - self.lattice[0][2]]) # 1: A+a->B
        ab.append([ab[0][0] - self.lattice[1][0], ab[0][1] - self.lattice[1][1], ab[0][2] - self.lattice[1][2]]) # 2: A+b->B
        ab.append([ab[0][0] - self.lattice[2][0], ab[0][1] - self.lattice[2][1], ab[0][2] - self.lattice[2][2]]) # 3: A+c->B
        ab.append([ab[1][0] - self.lattice[1][0], ab[1][1] - self.lattice[1][1], ab[1][2] - self.lattice[1][2]]) # 4: A+a+b->B
        ab.append([ab[1][0] - self.lattice[2][0], ab[1][1] - self.lattice[2][1], ab[1][2] - self.lattice[2][2]]) # 5: A+a+c->B
        ab.append([ab[2][0] - self.lattice[2][0], ab[2][1] - self.lattice[2][1], ab[2][2] - self.lattice[2][2]]) # 6: A+b+c->B
        ab.append([ab[4][0] - self.lattice[2][0], ab[4][1] - self.lattice[2][1], ab[4][2] - self.lattice[2][2]]) # 7: A+a+b+c->B
        return min([(x[0]**2. + x[1]**2. + x[2]**2.)**.5 for x in ab])

    def adjacent_matrix(self, r_min=0., r_max=1.9):
        n = len(self.ion)
        adj_mat = [[0]*n for i in range(n)]
        for i in range(n):
            for j in range(1+i, n): 
                 if r_min <= self.distance(i, j) <= r_max:
                      adj_mat[i][j] = adj_mat[j][i] = 1
        return adj_mat         
             
