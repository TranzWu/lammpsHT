# N independent runs. {name: ensemble_runs}

import os
from os import system
from joblib import Parallel, delayed
import sys
import numpy as np
#insert parameters here
njobs = 1
#insert pretreatment
def run(k):
    #insert code here
    os.system('python change_parameter.py --input auto.in --line pressure --index 5 --new [-0.5, -1.0, -1.5, -2, -2.5, -3]')
 	os.system("change_parameter.py --input hole.in --line hole --index "3 4" --new " + new)
    #insert post-processing
Parallel(n_jobs=jobs)(delayed(run)(i) for i in range(N))