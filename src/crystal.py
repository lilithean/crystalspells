#!/usr/bin/env python

import sys, os

import numpy as np

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
            output += 'direct\n'
            output += '\n'.join(['%12.7f   %12.7f   %12.7f' % (x[0], x[1], x[2]) for y in pos_list for x in y])   

        if not fname:
            print output
        else:
            with open(fname, 'w') as fid:
                fid.write(output)

s = Crystal()
s.from_file(sys.argv[1])
s.to()
