
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
from itertools import product

from analysis.learning_math import time_to_hit, hits_per_min, relative_number_hits
from analysis.learning_plots import plot_tth, plot_hpm
from utils.general_constants import GeneralConstants, obtain_session_name
from utils.loader import SessionLoader

from analysis.analysis_constants import learning_directory, plots_directory, path_learning_stats_file_name, \
    path_learning_curve_file_name
from analysis.analysis_command import AnalysisConfiguration
from utils.loader import load_sessions_filename, load_occupancy, load_names_dates, load_hits


def population_occupancy():
    df_sessions = load_sessions_filename()
    df_occupancy, df_occupancy_t2, df_base_occupancy, df_base_occupancy_t2 = load_occupancy()
    df_hits, df_hits_t2 = load_hits()
    mice_names, dates, type_pre_trainings = load_names_dates()
    df_index_occupancy = (df_occupancy - df_occupancy_t2)/df_occupancy
    df_index_occupancy_relative_baseline = (df_occupancy - df_base_occupancy)/df_occupancy
    df_index_occupancy_relative_baseline_and_t2 = df_index_occupancy_relative_baseline / \
                                                   ((df_occupancy_t2 - df_base_occupancy_t2) / df_occupancy_t2)
    df_index_hits = (df_hits - df_hits_t2) / df_hits
    occupancy_columns = ['Occupancy_t2_index', 'Occupancy_base_index', 'Occupancy_base_t2_index']
    multiindex_occupancy = pd.MultiIndex.from_product((type_pre_trainings, occupancy_columns))
    df_learning_occupancy = pd.DataFrame(index=mice_names, columns=multiindex_occupancy)
    for mice_name in mice_names:
        for date in dates:
            pre_training = df_sessions.loc[date, (mice_name, '1_exp')]
            if pre_training is not None:
                if np.nansum(df_learning_occupancy.loc[mice_name, (pre_training, 'Occupancy_t2_index')]) == 0:
                    df_learning_occupancy.loc[mice_name, (pre_training, 'Occupancy_t2_index')] =\
                        [df_index_occupancy.loc[date, mice_name]]
                else:
                    df_learning_occupancy.loc[mice_name, (pre_training, 'Occupancy_t2_index')].append(
                        df_index_occupancy.loc[date, mice_name])
                if np.nansum(df_learning_occupancy.loc[mice_name, (pre_training, 'Occupancy_base_index')]) == 0:
                    df_learning_occupancy.loc[mice_name, (pre_training, 'Occupancy_base_index')] =\
                        [df_index_occupancy_relative_baseline.loc[date, mice_name]]
                else:
                    df_learning_occupancy.loc[mice_name, (pre_training, 'Occupancy_base_index')].append(
                        df_index_occupancy_relative_baseline.loc[date, mice_name])
                if np.nansum(df_learning_occupancy.loc[mice_name, (pre_training, 'Occupancy_base_t2_index')]) == 0:
                    df_learning_occupancy.loc[mice_name, (pre_training, 'Occupancy_base_t2_index')] =\
                        [df_index_occupancy_relative_baseline_and_t2.loc[date, mice_name]]
                else:
                    df_learning_occupancy.loc[mice_name, (pre_training, 'Occupancy_base_t2_index')].append(
                        df_index_occupancy_relative_baseline_and_t2.loc[date, mice_name])


def population_learning():
    df_sessions = load_sessions_filename()
    mice_names, dates, type_pre_trainings = load_names_dates()
    create_df = True

    for mice_name in mice_names:
        for date in dates:
            pre_training = df_sessions.loc[date, (mice_name, '1_exp')]
            if pre_training is not None:
                df_stats = pd.read_parquet(path_learning_stats_file_name(obtain_session_name(mice_name, date),
                                                                         GeneralConstants.local_dir))
                df_curve = pd.read_parquet(path_learning_curve_file_name(obtain_session_name(mice_name, date),
                                                                         GeneralConstants.local_dir))
                if create_df:
                    learning_stat = df_stats.columns
                    learning_curve = df_curve.columns
                    multiindex_learning = pd.MultiIndex.from_product((type_pre_trainings, learning_stat))
                    multiindex_curve = pd.MultiIndex.from_product((type_pre_trainings, learning_curve))
                    df_learning_stats = pd.DataFrame(index=mice_names, columns=multiindex_learning)
                    df_learning_curve = pd.DataFrame(index=mice_names, columns=multiindex_curve)
                    create_df = False
                for ls in learning_stat:
                    try:
                        df_learning_stats.loc[mice_name, (pre_training, ls)].append(df_stats[ls].values[0])
                    except AttributeError:
                        df_learning_stats.loc[mice_name, (pre_training, slice(None))] = df_stats.values
                        break
                for cc in learning_curve:
                    try:
                        df_learning_curve.loc[mice_name, (pre_training, cc)].append(df_curve[cc].values[0])
                    except AttributeError:
                        df_learning_curve.loc[mice_name, (pre_training, slice(None))] = df_curve.values
                        break








