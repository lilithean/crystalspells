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
# 1. EIGENVAL: 
#   Will read eigenvalues from the band-structure calculation.
#
# 2. DOSCAR: 
#   Will read density of states from the mesh grid calculation. 
#   Also read fermi level, and all energies will be shifted. 
#   Can use a band-structure calculation DOSCAR instead
#

import sys
sys.path.append('/projects/academic/ezurek/xiaoyu/src/crystalspells/src/')
import numpy as np
from crystal import *

# read eigenvalues from eigenval
with open('EIGENVAL', 'r') as fid:
    eigen_data = fid.readlines()
n_elec, n_kpts, n_bnd = (int(x) for x in eigen_data[5].split())
kpoints = [[float(x) for x in y.split()[:3]] for y in eigen_data[7::n_bnd+2]]

# read fermi-level and dos from doscar 
with open('DOSCAR', 'r') as fid:
    dos_data = fid.readlines()
    e_fermi = float(dos_data[5].split()[3])
 
cbm = e_fermi + 100.0
vbm = e_fermi - 100.0
for i in range(n_bnd):
    j = 8 + i*(n_bnd+2)
    k = 0
    while (k < n_bnd) and (float(eigen_data[j+k].split()[1]) < e_fermi):
         k += 1
    if cbm > float(eigen_data[j+k].split()[1]):
        cbm = float(eigen_data[j+k].split()[1]) 
    if vbm < float(eigen_data[j+k-1].split()[1]):
        vbm = float(eigen_data[j+k-1].split()[1])
print cbm, vbm
print cbm-vbm
