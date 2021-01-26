# to plot the results of learning_math per individual sessions

import numpy as np
import utils.utils_plots as ut_plots
from pathlib import Path
from utils.utils_math import sliding_mean


def plot_tth(tth_pm_sec: np.array, temp_array: np.array, folder_path: Path, session_name: str):
    """ function to plot time to hit """
    fig1, ax1 = ut_plots.open_plot()
    ax1.plot(temp_array[1:], tth_pm_sec, '*')
    ax1.set_xlim([temp_array[0], temp_array[-1]])
    ax1.set_xlabel('Time elapsed (min)')
    ax1.set_ylabel('Time to hit (sec)')
    ut_plots.save_plot(fig1, ax1, var_y='time_to_hit', var_x=session_name, folder_path=folder_path, set_labels=False)


def plot_hpm(hpm: np.array, temp_array: np.array, sliding_window: int, folder_path: Path, session_name: str):
    """ function to plot hpm """
    fig1, ax1 = ut_plots.open_plot()
    ax1.plot(temp_array[1:], sliding_mean(hpm, sliding_window))
    ax1.set_xlabel('Time elapsed (min)')
    ax1.set_ylabel('hits per min')
    ut_plots.save_plot(fig1, ax1, var_y='hits_per_min', var_x=session_name, folder_path=folder_path, set_labels=False)
