#!/usr/bin/env python
import sys
import numpy as np

tol = 0.005

print "\nmessage: interpolation is not achieved in this script, please use a dense k-mesh else take your own risk\n"

print "_(:3 general information )_"
# read eigenvalues from eigenval
with open('EIGENVAL', 'r') as fid:
    eigen_data = fid.readlines()
n_elec, n_kpts, n_bnd = (int(x) for x in eigen_data[5].split())
kpoints = [[float(x) for x in y.split()[:3]] for y in eigen_data[7::n_bnd+2]]
print "  n_bnds = %i\n  n_kpts = %i\n  n_elec = %i" % (n_bnd, n_kpts, n_elec)

# read fermi-level and dos from doscar 
with open('DOSCAR', 'r') as fid:
    dos_data = fid.readlines()
    e_fermi = float(dos_data[5].split()[3])
print "  e_fermi = %.3f eV\n" % e_fermi

bands = []
for i in range(n_bnd):
    bands.append([float(eigen_data[8+i+x*(n_bnd+2)].split()[1]) for x in range(n_kpts)])

print "_(:3 band list )_"
print "message: energies below are already shifted to Fermi level"
print "%3s   %7s %8s %8s %8s   %7s %8s %8s %8s" % ("#", "e_min", "kx", "ky", "kz", "e_max", "kx", "ky", "kz")
for i in range(n_bnd):
    b_max = max(bands[i])
    b_min = min(bands[i])
    wi = bands[i].index(b_min)
    wj = bands[i].index(b_max)
    output = "%3i" % (i + 1)
    output += "   %7.3f" % (b_min-e_fermi)
    output += " %8.5f %8.5f %8.5f" % (kpoints[wi][0], kpoints[wi][1], kpoints[wi][2])
    output += "   %7.3f" % (b_max-e_fermi)
    output += " %8.5f %8.5f %8.5f" % (kpoints[wj][0], kpoints[wj][1], kpoints[wj][2])
    print output
print

print "_(:3 frontier orbital )_"
band_type = [] # positive = ib, 0 = vb, -1 = cb 
for i in range(n_bnd):
    if max(bands[i]) <= e_fermi + tol:
        band_type.append(i+1)
    elif min(bands[i]) - tol < e_fermi < max(bands[i]) + tol:
        band_type.append(0)
    elif min(bands[i]) >= e_fermi - tol:
        band_type.append(-1)

if any([x==0 for x in band_type]):
    print "  ! conductor"
    print "  bg= 0.000"
    
else:
    vb = max(band_type)-1
    cb = max(band_type)
    vbm = sorted(list(enumerate(bands[vb])), key=lambda x: -x[1])
    cbm = sorted(list(enumerate(bands[cb])), key=lambda x: x[1])
    bg = cbm[0][1] - vbm[0][1]

    print "     cbm            kx         ky         kz         vbe" 
    for i in cbm[:10]:
        print "%  8.3f      %8.5f   %8.5f   %8.5f    %8.3f" % (i[1]-e_fermi, kpoints[i[0]][0], kpoints[i[0]][1], kpoints[i[0]][2], bands[vb][i[0]]-e_fermi)
    
    print "     vbm            kx         ky         kz         cbe"
    for i in vbm[:10]:
        print "%  8.3f      %8.5f   %8.5f   %8.5f    %8.3f" % (i[1]-e_fermi, kpoints[i[0]][0], kpoints[i[0]][1], kpoints[i[0]][2], bands[cb][i[0]]-e_fermi)
    print "bg= %.3f" % bg
