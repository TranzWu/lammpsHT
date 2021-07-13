# N independent runs. {name: ensemble_runs}

import os
from os import system
from joblib import Parallel, delayed
import sys
import numpy as np
#insert parameters here
N_ensemble = 5
cores = 4
njobs = 5
#insert pretreatment
os.system('mkdir results')
def run(k):
    #insert code here
    os.system('python change_parameter.py --input auto.in --line velocity_placeolder --index 4 --new random')
    os.system('python change_parameter.py --input auto.in --line interior --index 4 --new random')
    os.system('python change_parameter.py --input auto.in --line bulk --index 4 --new random')
    os.system(f'mpirun --oversubscribe -np {cores} lmp_mpi -in auto.in > output.lammps') 	os.system("change_parameter.py --input hole.in --line hole --index "3 4" --new " + new)
    #insert post-processing
    os.system('calculate.py --output result_{k}')
    os.system('mv result_* results')
Parallel(n_jobs=jobs)(delayed(run)(i) for i in range(N))