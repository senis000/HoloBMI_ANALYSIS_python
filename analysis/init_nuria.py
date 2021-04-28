# small script to test stuff in ipython
# (yeah I know there are better ways to do it, but don't teach an old dog new tricks)

# %load_ext autoreload
# %autoreload 2

import os
import copy
import pickle
import pandas as pd
import numpy as np
import warnings
import h5py
import matplotlib.pyplot as plt
import scipy.stats as stats
from matplotlib import interactive
from scipy import signal, sparse, ndimage, spatial
from PIL import Image

from utils.general_constants import *
from analysis.analysis_constants import *
from utils.loader import load_sessions_filename
from utils.loader import SessionLoader
from analysis.analysis_command import AnalysisConfiguration
from analysis.run_at_night import run_at_night

interactive(True)
warnings.filterwarnings("ignore", message="The PostScript backend does not support transparency")
df = load_sessions_filename()
session_date = '191107'
mice_name = 'NVI17'
loader = SessionLoader(session_date, mice_name)

