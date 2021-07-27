# N independent runs. {name: ensemble_runs}

import os
from os import system
from joblib import Parallel, delayed
import sys
import numpy as np
#insert parameters here
line_0_0 = [5, 7, 9, 11, 13, 15, 17, 19]
line_0_1 = [5, 7, 9, 11, 13, 15, 17, 19]
N_ensemble = 8
njobs = 2
#insert pretreatment
def run(k):
    #insert preheat
    os.system(f'mkdir layer3_{k}')
    os.system(f'cp piston.in layer_* run_this* layer3_{k}')
    os.chdir(f'layer3_{k}')
    #insert code here
    l_0_0 = line_0_0[k]
    os.system(f'change_parameter.py --input piston.in --line hole_up --index 3 --new {l_0_0}')
    l_0_1 = line_0_1[k]
    os.system(f'change_parameter.py --input piston.in --line hole_up --index 4 --new {l_0_1}')
    #insert post-processing
    os.system(f'python layer_2.py')
    os.chdir('..')
Parallel(n_jobs=njobs)(delayed(run)(i) for i in range(N_ensemble))