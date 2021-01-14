# some useful functions

from pathlib import Path
import pandas as pd
import numpy as np
from scipy.io import loadmat
from typing import Union, Optional


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


def from_matlab_file_to_dict(filename: Path) -> dict:
    """ takes a filename path and returns a numpy workable dictionary containing the variables """
    mat = loadmat(str(filename))
    clean_dict = from_mat_dict(mat)
    return clean_dict


def from_mat_dict(mat: dict, keys: Optional[str] = None) -> dict:
    """ takes a mat with matlab mess and cleans it """
    out_dict = {}
    if keys is None:
        keys = mat.keys()
    for key in keys:
        print(key)
        if type(mat[key]) == np.ndarray:
            if len(mat[key]) > 0:
                key_variables = mat[key].dtype.names
                if key_variables is None:
                    if mat[key].dtype == np.dtype('O'):
                        out_dict[key] = np.squeeze(mat[key][0][0])
                    else:
                        out_dict[key] = np.squeeze(mat[key])
                elif 'label' in key_variables:
                    if mat[key].dtype == np.dtype('O'):
                        out_dict[key] = _mat_with_labels(key_variables, mat[key][0][0])
                    else:
                        out_dict[key] = _mat_with_labels(key_variables, mat[key])
                else:
                    out_dict[key] = from_mat_dict(mat[key][0][0], key_variables)
            else:
                out_dict[key] = mat[key]

    return out_dict


def _mat_with_labels(key_variables: tuple, in_dict: dict) -> dict:
    """ to take care of very weird mats with labels embeded deep """
    possible_labels = np.prod(in_dict[key_variables[0]].shape)
    if 'label' in key_variables:
        updated_key_variables = list(key_variables)
        updated_key_variables.remove('label')
    else:
        updated_key_variables = key_variables
    dict_key = {}

    for ll in np.arange(possible_labels):
        aux_label = in_dict['label'][0][ll][0]
        if len(aux_label) == 0:
            aux_label = 'n/a'
        if len(updated_key_variables) == 1:
            dict_key[aux_label] = np.squeeze(in_dict[updated_key_variables[0]][0][ll])
        else:
            dict_key[aux_label] = {}
            for key_var in updated_key_variables:
                dict_key[aux_label][key_var] = np.squeeze(in_dict[key_var][0][ll])
    return dict_key



