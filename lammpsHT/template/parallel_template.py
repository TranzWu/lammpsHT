# N independent runs. {name: ensemble_runs}

import os
from os import system
from joblib import Parallel, delayed
import sys
import numpy as np
#insert parameters here
#insert pretreatment
def run(k):
    #insert preheat
    #insert code here
    #insert post-processing
Parallel(n_jobs=njobs)(delayed(run)(i) for i in range(N_ensemble))