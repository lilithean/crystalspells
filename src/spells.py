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

class Elastic(object):

    """
    The idea in this script was originally proposed in:
    Le Page, Y., & Saxe, P. (2002). Symmetry-general least-squares extraction of elastic data for strained materials from ab initio calculations of stress. Physical Review B, 65(10), 104104.
    """

    def __init__(self):
        deform = []
        strain = []
        stress = []

def product3(A, B):
    return [[A[0][0]*B[0][0]+A[0][1]*B[1][0]+A[0][2]*B[2][0],
             A[0][0]*B[0][1]+A[0][1]*B[1][1]+A[0][2]*B[2][1],
             A[0][0]*B[0][2]+A[0][1]*B[1][2]+A[0][2]*B[2][2]],
            [A[1][0]*B[0][0]+A[1][1]*B[1][0]+A[1][2]*B[2][0],
             A[1][0]*B[0][1]+A[1][1]*B[1][1]+A[1][2]*B[2][1],
             A[1][0]*B[0][2]+A[1][1]*B[1][2]+A[1][2]*B[2][2]],
            [A[2][0]*B[0][0]+A[2][1]*B[1][0]+A[2][2]*B[2][0],
             A[2][0]*B[0][1]+A[2][1]*B[1][1]+A[2][2]*B[2][1],
             A[2][0]*B[0][2]+A[2][1]*B[1][2]+A[2][2]*B[2][2]]]
             
def connected_components(adj_mat):

    visited = [False] * len(adj_mat)
    cluster = []

    def dfs(i):
        visited[i] = True
        cluster[-1].append(i)
        for j in range(len(adj_mat)):
            if adj_mat[i][j] == 1:
                if not visited[j]:
                    dfs(j)

    for i in range(len(adj_mat)):
        if not visited[i]:
            cluster.append([])
            dfs(i)

    return cluster


