# to analyze different learning stats.

import itertools
import numpy as np
import pandas as pd
import scipy.stats as stats
from typing import Tuple


def time_to_hit(array_hits: np.array, bins_min: np.array) -> Tuple[np.array, np.array]:
    """ returns time between hits (tth) as value and as array with the value on the position where the hit happened """
    tth = list((sum(1 for _ in group) for value, group in itertools.groupby(array_hits) if value == 0))
    tth = np.asarray(tth)
    tth_array = np.zeros(array_hits.shape[0])
    hits_location = np.where(array_hits == 1)[0]
    for hh, hit in enumerate(hits_location):
        tth_array[hit] = tth[hh]
    tth_array[tth_array == 0] = np.nan
    tth_pm, _, _ = stats.binned_statistic(np.arange(tth_array.shape[0]), tth_array, np.nanmean, bins_min)
    return tth, tth_pm


def hits_per_min(array_hits: np.array, bins_min: np.array) -> np.array:
    """ returns hits per minute as array with each bin being 1 minute """
    hpm, _, _ = stats.binned_statistic(np.arange(array_hits.shape[0]), array_hits, 'sum', bins_min)
    return hpm


def relative_number_hits(number_hits_calibration: int, number_frames_baseline: int, array_hits: np.array,
                         frame_rate: float) -> pd.Series:
    """ return the percentage of increase on hits from baseline, being baseline the calibration, 5, 10, 15min of exp"""
    s = pd.Series(index=['increase_calibration', 'increase_5min', 'increase_10min', 'increase_15min',
                         'learning_index_calibration', 'learning_index_5min', 'learning_index_10min',
                         'learning_index_15min'])
    expected_hits_calibration = array_hits.shape[0]/number_frames_baseline*number_hits_calibration
    s['increase_calibration'] = (np.nansum(array_hits) - expected_hits_calibration) / expected_hits_calibration
    s['learning_index_calibration'] = (np.nansum(array_hits) - expected_hits_calibration) / np.nansum(array_hits)
    baseline_hits_5min = np.nansum(array_hits[:frame_rate*5*60])
    s['increase_5min'] = (np.nansum(array_hits) - baseline_hits_5min) / baseline_hits_5min
    s['learning_index_5min'] = (np.nansum(array_hits) - baseline_hits_5min) / np.nansum(array_hits)
    baseline_hits_10min = np.nansum(array_hits[:frame_rate * 10 * 60])
    s['increase_10min'] = (np.nansum(array_hits) - baseline_hits_10min) / baseline_hits_10min
    s['learning_index_10min'] = (np.nansum(array_hits) - baseline_hits_10min) / np.nansum(array_hits)
    baseline_hits_15min = np.nansum(array_hits[:frame_rate * 15 * 60])
    s['increase_15min'] = (np.nansum(array_hits) - baseline_hits_15min) / baseline_hits_15min
    s['learning_index_15min'] = (np.nansum(array_hits) - baseline_hits_15min) / np.nansum(array_hits)
    return s





