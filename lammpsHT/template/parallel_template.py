# N independent runs. {name: ensemble_runs}

import os
from os import system
from joblib import Parallel, delayed
import sys
#inser parameters here

def run(k):
    #inser code here
 	os.system("change_parameter.py --input hole.in --line hole --index "3 4" --new " + new)

Parallel(n_jobs=jobs)(delayed(run)(i) for i in range(N))