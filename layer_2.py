# N independent runs. {name: ensemble_runs}

import os
from os import system
from joblib import Parallel, delayed
import sys
import numpy as np
#insert parameters here
line_0_0 = [200, 400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000]
N_ensemble = 10
njobs = 5
#insert pretreatment
def run(k):
    #insert preheat
    os.system(f'mkdir layer2_{k}')
    os.system(f'cp piston.in layer_* run_this* layer2_{k}')
    os.chdir(f'layer2_{k}')
    #insert code here
    l_0_0 = line_0_0[k]
    os.system(f'change_parameter.py --input piston.in --line interior --index 3 --new {l_0_0}')
    #insert post-processing
    os.system(f'python layer_1.py')
    os.chdir('..')
Parallel(n_jobs=njobs)(delayed(run)(i) for i in range(N_ensemble))