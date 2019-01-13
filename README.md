# crystalspells

So this is basically a tool package for VASP calculation. \
Currently I have executables below in the bin folder:

1. band_structure.py \
   A script read the VASP output and generate the matplotlib figure. \
   It explains itself in the beginning of the file.
   
2. reciprocal.py \
   Read a poscar format and calculate the reciprocal lattice.
   
3. supercell.py \
   This is for test purpose... \
   Believe that you all have beautiful scripts to generate supercell. \
   But the function in the core script (src/crystal.py) has full function of making supercell.

4. connectivity.py \
   An efficient BFS algorithm to calculate the connectivity of the crystal. \
   It will create a 2x2x2 supercell first, so if it gives "8" that means you have a single molecule in the lattice, which is not connecting to it's own image. \
   In the same way: 1 means a bulk, 2 means a slab, 4 means chains, many means emmmmmm...... lol  
   One parameter "r_cut" is taken from the user input, which defines the cutoff of the radius.
   
5. naive_kpts.py \
   This one basically do two things: \
   first, do the same task as vasp does on generating a [fully automatic meshgrid](https://cms.mpi.univie.ac.at/vasp/vasp/Automatic_k_mesh_generation.html). \
   second, redistribute the same number of total k-points in propotional to the inverse of the length of the real space lattice.\
   This will avoid the [VERY BAD NEWS of IBZKPT](https://www.error.wiki/VERY_BAD_NEWS!_internal_error_in_subroutine_IBZKPT)
   

*Xiaoyu Wang* (xwang224@buffalo.edu) \
Department of Wizardary and Alchemical Engineering \
University at Buffalo
