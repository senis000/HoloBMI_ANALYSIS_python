# Main wrap of all other analysis to be run in a day


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


def one_function_to_run_them_all(session_date, mice_name):
    """ function to run all the analysis on the same mice """
    loader = SessionLoader(session_date, mice_name)

    # get the learning
    df_learning_measures = learning_wrap(loader)


def learning_wrap(loader: SessionLoader):
    """ Function to wrap around the learning functions """

    # some variables we need
    frame_rate = GeneralConstants.frame_rate
    target_cal = loader.experiment_variables.dict_target_calibration()
    number_hits_calibration = target_cal['num_valid_hits']
    baseline_dict = loader.experiment_variables.dict_baseline()
    aux_base = np.sum(baseline_dict['baseActivity'], 0)
    number_frames_baseline = aux_base[~np.isnan(aux_base)].shape[0]
    array_hits = loader.experiment_variables.array_hits()
    bins_min = np.arange(0, array_hits.shape[0], frame_rate * AnalysisConfiguration.bin_size_learning * 60)

    # obtaining the learning values
    s_stats = relative_number_hits(number_hits_calibration, number_frames_baseline, array_hits, frame_rate)

    df_stats = pd.DataFrame(s_stats).transpose()
    df_stats.to_parquet(path_learning_stats_file_name(loader.session_name, GeneralConstants.local_dir))

    # obtaining the learning curves
    tth, tth_pm = time_to_hit(array_hits, bins_min)
    hpm = hits_per_min(array_hits, bins_min)
    s_curve = pd.Series(dtype=float)
    s_curve['tth'] = tth
    s_curve['tth_pm'] = tth_pm
    s_curve['hpm'] = hpm
    df_curve = pd.DataFrame(s_curve).transpose()
    df_curve.to_parquet(path_learning_curve_file_name(loader.session_name, GeneralConstants.local_dir))

    # plot if required
    if AnalysisConfiguration.to_plot:
        learning_dir_plots = learning_directory(plots_directory(AnalysisConfiguration.local_dir))
        if not learning_dir_plots.exists():
            learning_dir_plots.mkdir()

        plot_tth(tth_pm/frame_rate, bins_min/frame_rate/60, learning_dir_plots,  loader.session_name)
        plot_hpm(hpm, bins_min/frame_rate/60, AnalysisConfiguration.sliding_window, learning_dir_plots,
                 loader.session_name)

    return df_stats


def learning_features(loader: SessionLoader):
    """ Function to retrieve all possible relevant features that could affect learning """
    s_features = pd.Series(dtype=float)
    pretraining_dict = loader.experiment_variables.dict_pretraining()
    s_features['holo_hits'] = np.nansum(pretraining_dict['data']['holoHits'])
    s_features['holo_rewards'] = np.nansum(pretraining_dict['data']['holoVTA'])










