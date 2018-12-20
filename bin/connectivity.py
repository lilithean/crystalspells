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

from crystal import *

if len(sys.argv) < 3:
    r_cut = 1.80
else:
    r_cut = float(sys.argv[2])

A = Crystal()
A.from_file(sys.argv[1])
print len(connected_components(A.adjacent_matrix(r_max=r_cut)))

