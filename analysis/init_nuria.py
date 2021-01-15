# small script to test stuff in ipython
# (yeah I know there are better ways to do it, but don't teach an old dog new tricks)

# %load_ext autoreload
# %autoreload 2

import os
import pandas as pd
import numpy as np
from matplotlib import interactive
from utils.general_constants import *
from analysis.analysis_constants import *

interactive(True)
df = session_dataframe()