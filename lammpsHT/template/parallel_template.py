# N independent runs. {name: ensemble_runs}

import os
from os import system
from joblib import Parallel, delayed
import sys
import numpy as np
#inser parameters here
#insert pretreatment
def run(k):
    #inser code here
 	os.system("change_parameter.py --input hole.in --line hole --index "3 4" --new " + new)
    #insert post-processing
Parallel(n_jobs=jobs)(delayed(run)(i) for i in range(N))