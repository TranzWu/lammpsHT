# N independent runs. {name: ensemble_runs}

import os
from os import system
from joblib import Parallel, delayed
import sys
import numpy as np
#insert parameters here
#insert pretreatment
def run(k):
    #insert code here
 	os.system("change_parameter.py --input hole.in --line hole --index "3 4" --new " + new)
    #insert post-processing
Parallel(n_jobs=jobs)(delayed(run)(i) for i in range(N))