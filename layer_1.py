# N independent runs. {name: ensemble_runs}

import os
from os import system
from joblib import Parallel, delayed
import sys
import numpy as np
#insert parameters here
cores = 4
N_ensemble = 5
njobs = 5
#insert pretreatment
def run(k):
    #insert preheat
    os.system(f'mkdir {k}')
    os.system(f'cp hole.in layer_* run_this {k}')
    os.chdir(f'{k}')
    #insert code here
    l_0_0 = 'random'
    os.system(f'change_parameter.py --input hole.in --line bulk --index 4 --new {l_0_0}')
    l_1_0 = 'random'
    os.system(f'change_parameter.py --input hole.in --line interior --index 4 --new {l_1_0}')
    l_2_0 = 'random'
    os.system(f'change_parameter.py --input hole.in --line velocity_placeolder --index 4 --new {l_2_0}')
    os.system(f'mpirun --oversubscribe -np {cores} lmp_mpi -in hole.in > output.lammps')
    #insert post-processing
    os.chdir('..')
Parallel(n_jobs=njobs)(delayed(run)(i) for i in range(N_ensemble))