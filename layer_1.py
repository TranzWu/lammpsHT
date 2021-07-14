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
os.system('mkdir results')
def run(k):
    #insert preheat
    #insert code here
    os.system('change_parameter.py --input hole.in --line velocity_placeolder --index 4 --new random')
    os.system('change_parameter.py --input hole.in --line interior --index 4 --new random')
    os.system('change_parameter.py --input hole.in --line bulk --index 4 --new random')
    os.system(f'mpirun --oversubscribe -np {cores} lmp_mpi -in hole.in > output.lammps')
    #insert post-processing
    os.system(f'calculate.py --output result_{k}')
    os.system(f'mv result_* results')
Parallel(n_jobs=njobs)(delayed(run)(i) for i in range(N_ensemble))