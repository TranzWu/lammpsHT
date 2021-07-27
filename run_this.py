# N independent runs. {name: ensemble_runs}

import os
from os import system
from joblib import Parallel, delayed
import sys
import numpy as np
#insert parameters here
line_0_0 = [-5, -7, -9]
N_ensemble = 3
njobs = 1
#insert pretreatment
def run(k):
    #insert preheat
    os.system(f'mkdir layer4_{k}')
    os.system(f'cp piston.in layer_* run_this* layer4_{k}')
    os.chdir(f'layer4_{k}')
    #insert code here
    l_0_0 = line_0_0[k]
    os.system(f'change_parameter.py --input piston.in --line fp_pressure --index 6 --new {l_0_0}')
    #insert post-processing
    os.system(f'python layer_3.py')
    os.chdir('..')
Parallel(n_jobs=njobs)(delayed(run)(i) for i in range(N_ensemble))