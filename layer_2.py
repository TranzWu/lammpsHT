# N independent runs. {name: ensemble_runs}

import os
from os import system
from joblib import Parallel, delayed
import sys
import numpy as np
#insert parameters here
line_0 = [[-0.1, -1.0, -1.5, -2, -2.5, -3], [-0.2, -1.0, -1.5, -2, -2.5, -3]]
N_ensemble = 6
njobs = 1
#insert pretreatment
def run(k):
    #insert preheat
    os.system(f'mkdir {k}')
    os.system(f'cp hole.in layer_* run_this {k}')
    os.chdir(f'{k}')
    #insert code here
    os.system(f'change_parameter.py --input hole.in --line initial_fluid --index 6 --new {line_0[1]}')
    os.system(f'change_parameter.py --input hole.in --line initial_fluid --index 5 --new {line_0[0]}')
    #insert post-processing
    os.system(f'python layer_1.py')
    os.chdir('..')
Parallel(n_jobs=njobs)(delayed(run)(i) for i in range(N_ensemble))