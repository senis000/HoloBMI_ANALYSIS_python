# function to create a df with all the general info of the sessions

import numpy as np
import os
import pandas as pd
from utils.general_constants import *


def find_files(df: pd.DataFrame) -> np.array:
    """ Function to return the number of files corresponding to that name"""
    animals = np.unique(df.columns.get_level_values(0))[1:]
    for animal in animals:
        df[animal, 'n_baseline'] = np.nan
        df[animal, 'n_bmi'] = np.nan
        df[animal, 'n_target_info'] = np.nan
        df[animal, 'n_target_cal'] = np.nan
        df[animal, 'n_holostim'] = np.nan
        df[animal, 'file_baseline'] = np.nan
        df[animal, 'file_pretraining'] = np.nan
        df[animal, 'file_training'] = np.nan
        df[animal, 'file_target_info'] = np.nan
        df[animal, 'file_target_cal'] = np.nan
        df[animal, 'file_holostim'] = np.nan
        for date in df.index:
            if type(df.loc[date, animal][0]) is str:
                aux_df = df.loc[date]['Day']
                list_files = os.listdir(files_directory(date, aux_df[aux_df.notna()][0], animal))
                baseline_files = []
                bmi_online_files = []
                bmi_target_files = []
                holostim_files = []
                target_calibration_files = []
                for file in list_files:
                    if (file[0:8] == 'Baseline') and (file[-3:] == 'mat') :
                        baseline_files.append(file)
                    elif (file[0:8] == 'BMI_onli') and (file[-3:] == 'mat'):
                        bmi_online_files.append(file)
                    elif (file[0:8] == 'BMI_targ') and (file[-3:] == 'mat'):
                        bmi_target_files.append(file)
                    elif (file[0:8] == 'holostim') and (file[-3:] == 'mat'):
                        holostim_files.append(file)
                    elif (file[0:8] == 'target_c') and (file[-3:] == 'mat'):
                        target_calibration_files.append(file)
                df.loc[date, (animal, 'n_baseline')] = len(baseline_files)
                if len(baseline_files) == 1:
                    df.loc[date, (animal, 'file_baseline')] = baseline_files[0]
                df.loc[date, (animal, 'n_bmi')] = len(bmi_online_files)
                if len(bmi_online_files) == 2:
                    df.loc[date, (animal, 'file_pretraining')] = bmi_online_files[0]
                    df.loc[date, (animal, 'file_training')] = bmi_online_files[1]
                else:
                    print('BMI: ' + animal + ' ' + date + ' ' + str(len(bmi_online_files)))
                df.loc[date, (animal, 'n_target_info')] = len(bmi_target_files)
                df.loc[date, (animal, 'file_target_info')] = bmi_target_files[-1]
                df.loc[date, (animal, 'n_target_cal')] = len(target_calibration_files)
                df.loc[date, (animal, 'file_target_cal')] = target_calibration_files[-1]
                df.loc[date, (animal, 'n_holostim')] = len(holostim_files)
                if len(holostim_files) == 1:
                    df.loc[date, (animal, 'file_holostim')] = holostim_files[0]
                else:
                    print('Holo: ' + animal + ' ' + date + ' ' + str(len(holostim_files)))