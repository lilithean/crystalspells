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

def dot_prod(a, b):
    return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]


def cross_prod(a, b):
    # a x b = (a2b3 - a3b2)i - (a1b3 - a3b1)j + (a1b2 - a2b1)k
    return [a[1]*b[2] - a[2]*b[1], -a[0]*b[2] + a[2]*b[0], a[0]*b[1] - a[1]*b[0]]

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
    """
    This is a simple dfs algorithm to check connectivity

    """

    visited = [False] * len(adj_mat)
    cluster = []

    def dfs(vertex):
        visited[vertex] = True
        cluster[-1].append(vertex)
        for j in range(len(adj_mat)):
            if adj_mat[vertex][j] == 1:
                if not visited[j]:
                    dfs(j)

    for i in range(len(adj_mat)):
        if not visited[i]:
            cluster.append([])
            dfs(i)

    return cluster

def cycle(adj_mat, vertex):
    """
    This is a simple dfs algorithm to find cycles around a given vertex
    """

    visited = [0] * len(adj_mat)
    visited[vertex] = 1

    def bfs(vertex, g=2):
        for j in range(len(adj_mat)):
            if adj_mat[vertex][j] == 1:
                if visited[j] == 0:
                    visited[j] == g
                    dfs(j, g+1)
                elif visited[j] == g:
                    pass







