# some useful functions

import pandas as pd
import numpy as np
from typing import Union


def sliding_mean(data_array: np.array, window: int = 5) -> np.array:
    """ program to smooth a graphic """
    data_array = np.array(data_array)
    new_list = []
    for i in range(np.size(data_array)):
        indices = range(max(i - window + 1, 0),
                        min(i + window + 1, np.size(data_array)))
        avg = 0
        for j in indices:
            avg = np.nansum([avg, data_array[j]])
        avg /= float(np.size(indices))
        new_list.append(avg)
    return np.array(new_list)


def calc_pvalue(p_value: float) -> str:
    """ returns a string with the pvalue ready to plot """
    if p_value <= 0.0005:
        p = '***'
    elif p_value <= 0.005:
        p = '**'
    elif p_value <= 0.05:
        p = '*'
    else:
        p = 'ns'
    return p


def function_sem(arr: np.array, is_array: bool = False) -> Union[int, np.array]:
    """ takes a numpy array and performs sem to it"""
    if is_array:
        return pd.DataFrame(arr).sem(0).values
    else:
        return pd.DataFrame(arr).sem(0).values[0]
