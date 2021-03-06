# some useful functions

from pathlib import Path
import numpy as np
from scipy.io import loadmat
from typing import Union, Optional

from utils.general_constants import *


def load_dict(session_date: str, day: str, mice_name: str, file_name: str) -> dict:
    return from_matlab_file_to_dict(
        files_directory(session_date, day, mice_name) / file_name)


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
