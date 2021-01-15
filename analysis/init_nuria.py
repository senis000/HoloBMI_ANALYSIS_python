# small script to test stuff in ipython
# (yeah I know there are better ways to do it, but don't teach an old dog new tricks)

# %load_ext autoreload
# %autoreload 2


import os
import datetime
import h5py
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from matplotlib import interactive
from typing import Dict, Tuple, Optional, List
import warnings
from analysis.analysis_constants import *
from analysis.analysis_command import AnalysisConfiguration

interactive(True)
local_dir_data = local_analysis_directory(AnalysisConstants.local_dir)
df = pd.read_excel(sessions_path(local_dir_data), header=[0, 1], index_col=0)
df.index = df.index.astype(str)