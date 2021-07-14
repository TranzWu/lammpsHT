# N independent runs. {name: ensemble_runs}

import os
from os import system
from joblib import Parallel, delayed
import sys
import numpy as np
#insert parameters here
line_0_0 = [-0.1, -1.0, -1.5, -2, -2.5, -3]
line_0_1 = [-0.2, -1.0, -1.5, -2, -2.5, -3]
line_1_0 = [-0.3, -1.0, -1.5, -2, -2.5, -3]
line_1_1 = [-0.4, -1.0, -1.5, -2, -2.5, -3]
N_ensemble = 6
njobs = 1
#insert pretreatment
def run(k):
    #insert preheat
    os.system(f'mkdir {k}')
    os.system(f'cp hole.in layer_* run_this {k}')
    os.chdir(f'{k}')
    #insert code here
    os.system(f'change_parameter.py --input hole.in --line random_stuff --index 7 --new line_1_1[{k}]')
    os.system(f'change_parameter.py --input hole.in --line random_stuff --index 4 --new line_1_0[{k}]')
    os.system(f'change_parameter.py --input hole.in --line initial_fluid --index 6 --new line_0_1[{k}]')
    os.system(f'change_parameter.py --input hole.in --line initial_fluid --index 5 --new line_0_0[{k}]')
    #insert post-processing
    os.system(f'python layer_1.py')
    os.chdir('..')
Parallel(n_jobs=njobs)(delayed(run)(i) for i in range(N_ensemble))