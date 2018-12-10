#!/usr/bin/env python

import sys, os

import numpy as np

class Elastic(object):

    """
    The idea in this script was originally proposed in:
    Le Page, Y., & Saxe, P. (2002). Symmetry-general least-squares extraction of elastic data for strained materials from ab initio calculations of stress. Physical Review B, 65(10), 104104.
    """

    def __init__(self):
        
