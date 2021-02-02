import os
import posixpath
import tempfile
import pickle
import datetime
import pendulum
import h5py
import warnings
import logging
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from matplotlib import interactive

from analysis.learning_math import time_to_hit, hits_per_min, relative_number_hits
from analysis.learning_plots import plot_tth, plot_hpm
from utils.general_constants import GeneralConstants
from utils.loader import SessionLoader

from analysis.analysis_constants import learning_directory, plots_directory, path_learning_stats_file_name, \
    path_learning_curve_file_name
from analysis.analysis_command import AnalysisConfiguration
from analysis.analysis_pipeline import one_function_to_run_them_all, learning_wrap
from utils.loader import load_sessions_filename, load_names_dates


def run_at_night():
    df_sessions = load_sessions_filename()
    mice_names, dates, type_pre_trainings, type_trainings = load_names_dates()
    for date in df_sessions.index:
        for mice_name in mice_names:
            pre_training = df_sessions.loc[date, (mice_name, '1_exp')]
            if pre_training is not None:
                one_function_to_run_them_all(session_date=date, mice_name=mice_name)



