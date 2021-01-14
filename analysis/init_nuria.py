# small script to test stuff in ipython
# (yeah I know there are better ways to do it, but don't teach an old dog new tricks)

# %load_ext autoreload
# %autoreload 2


import os
import posixpath
import tempfile
import datetime
import pendulum
import h5py
import numpy as np
import pandas as pd
import logging
import pyinform
import matplotlib.pyplot as plt
from matplotlib import interactive
from typing import Dict, Tuple, Optional, List
import warnings

interactive(True)