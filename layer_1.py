# N independent runs. {name: ensemble_runs}

import os
from os import system
from joblib import Parallel, delayed
import sys
import numpy as np
#insert parameters here
cores = 4
N_ensemble = 10
njobs = 2
#insert pretreatment
def run(k):
    #insert preheat
    os.system(f'mkdir layer1_{k}')
    os.system(f'cp piston.in layer_* run_this* layer1_{k}')
    os.chdir(f'layer1_{k}')
    #insert code here
    l_0_0 = 'random'
    os.system(f'change_parameter.py --input piston.in --line bulk --index 4 --new {l_0_0}')
    l_1_0 = 'random'
    os.system(f'change_parameter.py --input piston.in --line interior --index 4 --new {l_1_0}')
    l_2_0 = 'random'
    os.system(f'change_parameter.py --input piston.in --line velocity_placeholder --index 4 --new {l_2_0}')
    os.system(f'mpirun --oversubscribe -np {cores} lmp_mpi -in piston.in > output.lammps')
    #insert post-processing
    os.chdir('..')
Parallel(n_jobs=njobs)(delayed(run)(i) for i in range(N_ensemble))