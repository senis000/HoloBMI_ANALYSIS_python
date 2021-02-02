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
from matplotlib import cm
from matplotlib import interactive
from itertools import product

from analysis.learning_math import time_to_hit, hits_per_min, relative_number_hits
from analysis.learning_plots import plot_tth, plot_hpm
from utils.general_constants import GeneralConstants, obtain_session_name
from utils.loader import SessionLoader
import utils.utils_plots as ut_plots

from analysis.analysis_constants import learning_directory, plots_directory, path_learning_stats_file_name, \
    path_learning_curve_file_name, learning_occupancy_path
from analysis.analysis_command import AnalysisConfiguration
from utils.loader import load_sessions_filename, load_occupancy, load_names_dates, load_hits


def plot_population_occupancy_per_mice(folder_path):
    """ function to plot occupancy for each mice and experiment type """
    mice_names, _, type_pre_trainings, type_trainings = load_names_dates()
    for training in type_trainings:
        df_learning_occupancy = pd.read_parquet(learning_occupancy_path(AnalysisConfiguration.local_dir, training))
        for index_test in np.unique(df_learning_occupancy.columns.get_level_values(1)):
            # plot results per mice
            fig1, subplots = ut_plots.open_xsubplots(num_subplots=len(mice_names))
            for mm, mice in enumerate(mice_names):
                df_aux = pd.DataFrame(columns=['mean', 'sem'], index=type_pre_trainings)
                for pret in type_pre_trainings:
                    aux_val = df_learning_occupancy.loc[mice, (pret, index_test)]
                    if aux_val is not None:
                        df_aux.loc[pret, 'mean'] = np.nanmean(aux_val)
                        df_aux.loc[pret, 'sem'] = np.nanstd(aux_val) / np.sqrt(len(aux_val))
                ax = subplots[mm]
                ax.bar(df_aux.index, df_aux['mean'])
                ax.errorbar(df_aux.index, df_aux['mean'], yerr=df_aux['sem'], color='k')
                ax.set_ylabel(mice)
            ut_plots.save_plot(fig1, None, var_y=training, var_x=index_test + '_per_mice', folder_path=Path(folder_path),
                               set_labels=False)


def plot_population_occupancy_all(folder_path):
    """ function to plot occupancy for each mice and experiment type """
    mice_names, _, type_pre_trainings, type_trainings = load_names_dates()
    copper = cm.get_cmap('copper', len(mice_names))
    for training in type_trainings:
        df_learning_occupancy = pd.read_parquet(learning_occupancy_path(AnalysisConfiguration.local_dir, training))
        for index_test in np.unique(df_learning_occupancy.columns.get_level_values(1)):
            # plot results per mice
            fig1, ax1 = ut_plots.open_plot()
            df_aux = pd.DataFrame(columns=['mean', 'sem'], index=type_pre_trainings)
            for pret in type_pre_trainings:
                aux_array = np.full(len(mice_names), np.nan)
                for mm, mice in enumerate(mice_names):
                    aux_val = df_learning_occupancy.loc[mice, (pret, index_test)]
                    if aux_val is not None:
                        aux_array[mm] = np.nanmean(aux_val)
                        ax1.scatter(pret, aux_array[mm], color=copper(mm))
                df_aux.loc[pret, 'mean'] = np.nanmean(aux_array)
                df_aux.loc[pret, 'sem'] = np.nanstd(aux_array) / np.sqrt(len(aux_array))
            ax1.bar(df_aux.index, df_aux['mean'], color='gray')
            ax1.errorbar(df_aux.index, df_aux['mean'], yerr=df_aux['sem'], color='k')
            ax1.set_ylabel(index_test)
            ut_plots.save_plot(fig1, None, var_y=training, var_x=index_test, folder_path=Path(folder_path),
                               set_labels=False)











