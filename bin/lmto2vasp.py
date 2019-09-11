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

import sys
sys.path.append('/projects/academic/ezurek/xiaoyu/src/crystalspells/src/')
import numpy as np
from crystal import *

vec=[0.154308, 0.500000, 0.000000]
scl=4.254532
vec=[x/scl for x in vec]
A = Crystal()
A.from_file(sys.argv[1])
rec=A.reciprocal_lattice()
rec=np.linalg.inv(rec)
x = vec[0]*rec[0][0]+vec[1]*rec[1][0]+vec[2]*rec[2][0]
y = vec[0]*rec[0][1]+vec[1]*rec[1][1]+vec[2]*rec[2][1]
z = vec[0]*rec[0][2]+vec[1]*rec[1][2]+vec[2]*rec[2][2]
print "%8.6f %8.6f %8.6f" % (x,y,z)
