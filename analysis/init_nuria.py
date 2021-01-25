# small script to test stuff in ipython
# (yeah I know there are better ways to do it, but don't teach an old dog new tricks)

# %load_ext autoreload
# %autoreload 2

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import interactive
from utils.general_constants import *
from analysis.analysis_constants import *
from utils.loader import load_sessions_filename

interactive(True)
df = load_sessions_filename()
