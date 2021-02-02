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

import utils.utils_plots as ut_plots
from analysis.learning_math import time_to_hit, hits_per_min, relative_number_hits
from analysis.learning_plots import plot_tth, plot_hpm
from utils.general_constants import GeneralConstants, obtain_session_name
from utils.loader import SessionLoader
from utils.utils_math import sliding_mean
from analysis.analysis_constants import learning_directory, plots_directory, path_learning_stats_file_name, \
    path_learning_curve_file_name, learning_all_occupancy_path, learning_all_stats_path, learning_all_curves_path
from analysis.analysis_command import AnalysisConfiguration
from utils.loader import load_sessions_filename, load_occupancy, load_names_dates, load_hits


def plot_population_occupancy_per_mice(folder_path):
    """ function to plot occupancy for each mice and experiment type """
    mice_names, _, type_pre_trainings, type_trainings = load_names_dates()
    for training in type_trainings:
        df_learning_occupancy = pd.read_parquet(learning_all_occupancy_path(AnalysisConfiguration.local_dir, training))
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
            ut_plots.save_plot(fig1, None, var_y=training, var_x=index_test + '_per_mice',
                               folder_path=Path(folder_path),
                               set_labels=False)


def plot_population_occupancy_all(folder_path):
    """ function to plot occupancy for each mice and experiment type """
    mice_names, _, type_pre_trainings, type_trainings = load_names_dates()
    copper = cm.get_cmap('copper', len(mice_names))
    for training in type_trainings:
        df_learning_occupancy = pd.read_parquet(learning_all_occupancy_path(AnalysisConfiguration.local_dir, training))
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


def plot_population_learning_stats_per_mice(folder_path):
    """ function to plot occupancy for each mice and experiment type """
    mice_names, _, type_pre_trainings, type_trainings = load_names_dates()
    for training in type_trainings:
        df_learning_stats = pd.read_parquet(learning_all_stats_path(AnalysisConfiguration.local_dir, training))
        for index_test in np.unique(df_learning_stats.columns.get_level_values(1)):
            # plot results per mice
            fig1, subplots = ut_plots.open_xsubplots(num_subplots=len(mice_names))
            for mm, mice in enumerate(mice_names):
                df_aux = pd.DataFrame(columns=['mean', 'sem'], index=type_pre_trainings)
                for pret in type_pre_trainings:
                    aux_val = df_learning_stats.loc[mice, (pret, index_test)]
                    if aux_val is not None:
                        df_aux.loc[pret, 'mean'] = np.nanmean(aux_val)
                        df_aux.loc[pret, 'sem'] = np.nanstd(aux_val) / np.sqrt(len(aux_val))
                ax = subplots[mm]
                ax.bar(df_aux.index, df_aux['mean'])
                ax.errorbar(df_aux.index, df_aux['mean'], yerr=df_aux['sem'], color='k')
                ax.set_ylabel(mice)
            ut_plots.save_plot(fig1, None, var_y=training, var_x=index_test + '_per_mice',
                               folder_path=Path(folder_path),
                               set_labels=False)


def plot_population_learning_stats(folder_path):
    """ function to plot occupancy for each mice and experiment type """
    mice_names, _, type_pre_trainings, type_trainings = load_names_dates()
    copper = cm.get_cmap('copper', len(mice_names))
    for training in type_trainings:
        df_learning_stats = pd.read_parquet(learning_all_stats_path(AnalysisConfiguration.local_dir, training))
        for index_test in np.unique(df_learning_stats.columns.get_level_values(1)):
            # plot results per mice
            fig1, ax1 = ut_plots.open_plot()
            df_aux = pd.DataFrame(columns=['mean', 'sem'], index=type_pre_trainings)
            for pret in type_pre_trainings:
                aux_array = np.full(len(mice_names), np.nan)
                for mm, mice in enumerate(mice_names):
                    aux_val = df_learning_stats.loc[mice, (pret, index_test)]
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


def plot_population_learning_curve_per_mice(folder_path):
    """ function to plot occupancy for each mice and experiment type """
    frame_rate = GeneralConstants.frame_rate
    mice_names, _, type_pre_trainings, type_trainings = load_names_dates()
    bins_min = np.arange(0, frame_rate * AnalysisConfiguration.length_bin_array * 60,
                         frame_rate * AnalysisConfiguration.bin_size_learning * 60)
    for training in type_trainings:
        df_learning_curve = pd.read_parquet(learning_all_curves_path(AnalysisConfiguration.local_dir, training))
        index_tests = np.unique(df_learning_curve.columns.get_level_values(1))
        index_tests = index_tests[index_tests != 'bins_min']
        index_tests = index_tests[index_tests != 'tth']
        for index_test in index_tests:
            # plot results per mice
            for pret in type_pre_trainings:
                fig1, subplots = ut_plots.open_xsubplots(num_subplots=len(mice_names))
                for mm, mice in enumerate(mice_names):
                    aux_val = df_learning_curve.loc[mice, (pret, index_test)]
                    if aux_val is not None:
                        aux_array = np.full((len(aux_val), bins_min.shape[0]-1), np.nan)
                        for aa, aux_element in enumerate(aux_val):
                            bins_aux = df_learning_curve.loc[mice, (pret, 'bins_min')][aa]
                            if np.sum(bins_min[np.arange(bins_aux.shape[0])] - bins_aux) != 0:
                                raise ValueError('The value of bin array is different than expected!')
                            aux_array[aa, :bins_aux.shape[0] - 1] = sliding_mean(aux_element,
                                                                                 AnalysisConfiguration.sliding_window)
                        aux_mean = np.nanmean(aux_array, 0)
                        aux_sem = np.nanstd(aux_array, 0) / np.sqrt(aux_array.shape[0])
                        ax = subplots[mm]
                        ax.plot(bins_min[1:], aux_mean)
                        ax.fill_between(bins_min[1:], aux_mean - aux_sem, aux_mean + aux_sem, color='gray')
                        ax.set_ylabel(mice)
                ut_plots.save_plot(fig1, None, var_y=training, var_x=index_test + '_' + pret + '_per_mice',
                                   folder_path=Path(folder_path),
                                   set_labels=False)


def plot_population_learning_curve(folder_path):
    """ function to plot occupancy for each mice and experiment type """
    frame_rate = GeneralConstants.frame_rate
    mice_names, _, type_pre_trainings, type_trainings = load_names_dates()
    bins_min = np.arange(0, frame_rate * AnalysisConfiguration.length_bin_array * 60,
                         frame_rate * AnalysisConfiguration.bin_size_learning * 60)
    for training in type_trainings:
        df_learning_curve = pd.read_parquet(learning_all_curves_path(AnalysisConfiguration.local_dir, training))
        index_tests = np.unique(df_learning_curve.columns.get_level_values(1))
        index_tests = index_tests[index_tests != 'bins_min']
        index_tests = index_tests[index_tests != 'tth']
        for index_test in index_tests:
            # plot results per mice
            fig1, subplots = ut_plots.open_xsubplots(num_subplots=len(type_pre_trainings))
            for pp, pret in enumerate(type_pre_trainings):
                aux_all_mice = np.full((len(mice_names), bins_min.shape[0]-1), np.nan)
                for mm, mice in enumerate(mice_names):
                    aux_val = df_learning_curve.loc[mice, (pret, index_test)]
                    if aux_val is not None:
                        aux_array = np.full((len(aux_val), bins_min.shape[0]-1), np.nan)
                        for aa, aux_element in enumerate(aux_val):
                            bins_aux = df_learning_curve.loc[mice, (pret, 'bins_min')][aa]
                            if np.sum(bins_min[np.arange(bins_aux.shape[0])] - bins_aux) != 0:
                                raise ValueError('The value of bin array is different than expected!')
                            aux_array[aa, :bins_aux.shape[0] - 1] = sliding_mean(aux_element,
                                                                                 AnalysisConfiguration.sliding_window)
                        aux_all_mice[mm, :] = np.nanmean(aux_array, 0)
                aux_mean = np.nanmean(aux_all_mice, 0)
                aux_sem = np.nanstd(aux_all_mice, 0) / np.sqrt(aux_all_mice.shape[0])
                ax = subplots[pp]
                ax.plot(bins_min[1:], aux_mean)
                ax.fill_between(bins_min[1:], aux_mean - aux_sem, aux_mean + aux_sem, color='gray')
                ax.set_ylabel(pret)
                if index_test == 'hpm':
                    ax.set_ylim([0.2, 0.8])
                else:
                    ax.set_ylim([500, 2500])
            ut_plots.save_plot(fig1, None, var_y=training, var_x=index_test, folder_path=Path(folder_path),
                               set_labels=False)
