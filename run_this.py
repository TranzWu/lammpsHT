# N independent runs. {name: ensemble_runs}

import os
from os import system
from joblib import Parallel, delayed
import sys
import numpy as np
#insert parameters here
line_0_0 = [0, 1, 2, 3, 4]
N_ensemble = 5
njobs = 3
#insert pretreatment
def run(k):
    #insert preheat
    os.system(f'mkdir {k}')
    os.system(f'cp hole.in layer_* run_this {k}')
    os.chdir(f'{k}')
    #insert code here
    l_0_0 = line_0_0[k]
    os.system(f'change_parameter.py --input hole.in --line pressure --index 4 --new l_0_0')
    #insert post-processing
    os.system(f'python layer_2.py')
    os.chdir('..')
Parallel(n_jobs=njobs)(delayed(run)(i) for i in range(N_ensemble))