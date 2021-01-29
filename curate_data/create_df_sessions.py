# function to create a df with all the general info of the sessions

import numpy as np
import os
import pandas as pd
from pathlib import Path
from utils.general_constants import *


def find_files(df: pd.DataFrame) -> pd.DataFrame:
    """ Function to return the number and name of files corresponding to that name"""
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

    # for the sessions/files with more than one valid option. Checked manually
    # from looking at the files and checking with the mice_log and the .m files of each session
    df.loc['191007', ('NVI12', 'file_pretraining')] = 'BMI_online191007T145608.mat'
    df.loc['191007', ('NVI12', 'file_training')] = 'BMI_merged.mat'
    df.loc['191009', ('NVI12', 'file_pretraining')] = 'BMI_online191009T144910.mat'
    df.loc['191009', ('NVI12', 'file_training')] = 'BMI_online191009T153223.mat'
    df.loc['191025', ('NVI12', 'file_pretraining')] = 'BMI_merged.mat'
    df.loc['191025', ('NVI12', 'file_training')] = 'BMI_online191025T154101.mat'
    df.loc['191003', ('NVI13', 'file_pretraining')] = 'BMI_online191003T171028.mat'
    df.loc['191003', ('NVI13', 'file_training')] = 'BMI_online191003T175350.mat'
    df.loc['191001', ('NVI16', 'file_pretraining')] = 'BMI_online191001T195536.mat'
    df.loc['191001', ('NVI16', 'file_training')] = 'BMI_online191001T203900.mat'
    df.loc['191004', ('NVI16', 'file_pretraining')] = 'BMI_online191004T203809.mat'
    df.loc['191004', ('NVI16', 'file_training')] = 'BMI_online191004T212633.mat'
    df.loc['191005', ('NVI16', 'file_pretraining')] = 'BMI_online191005T204800.mat'
    df.loc['191005', ('NVI16', 'file_training')] = 'BMI_online191005T213208.mat'
    df.loc['191011', ('NVI16', 'file_pretraining')] = 'BMI_online191011T201508.mat'
    df.loc['191011', ('NVI16', 'file_training')] = 'BMI_online191011T205824.mat'
    df.loc['191025', ('NVI16', 'file_pretraining')] = 'BMI_merged.mat'
    df.loc['191025', ('NVI16', 'file_training')] = 'BMI_online191025T214847.mat'
    df.loc['191026', ('NVI16', 'file_pretraining')] = 'BMI_merged.mat'
    df.loc['191026', ('NVI16', 'file_training')] = 'BMI_online191026T213341.mat'
    df.loc['191028', ('NVI16', 'file_pretraining')] = 'BMI_online191028T204050.mat'
    df.loc['191028', ('NVI16', 'file_training')] = 'BMI_online191028T212555.mat'
    df.loc['191031', ('NVI16', 'file_pretraining')] = 'BMI_merged_pre.mat'
    df.loc['191031', ('NVI16', 'file_training')] = 'BMI_merged_bmi.mat'
    df.loc['191104', ('NVI13', 'file_baseline')] = 'BaselineOnline191104T165948.mat'
    df.loc['191106', ('NVI17', 'file_pretraining')] = 'BMI_online191106T224336.mat'
    df.loc['191106', ('NVI17', 'file_training')] = 'BMI_online191106T232637.mat'
    df.loc['191106', ('NVI22', 'file_baseline')] = 'BaselineOnline191106T142147.mat'
    df.loc['191212', ('NVI17', 'file_training')] = 'BMI_online191212T192539.mat'
    df.loc['191212', ('NVI20', 'file_training')] = 'BMI_online191212T225302.mat'
    df.loc['191212', ('NVI22', 'file_training')] = 'BMI_online191213T003135.mat'
    df.loc['191214', ('NVI17', 'file_training')] = 'BMI_online191214T175324.mat'
    df.loc['191214', ('NVI20', 'file_training')] = 'BMI_online191214T225319.mat'
    df.loc['191214', ('NVI22', 'file_training')] = 'BMI_online191214T200413.mat'
    df.loc['191214', ('NVI22', 'file_baseline')] = 'BaselineOnline191214T185954.mat'
    df.loc['191214', ('NVI20', 'file_pretraining')] = np.nan
    df = df.sort_index(axis=1)
    df.to_parquet(Path(curated_data_directory()) / 'session_filenames.parquet')
    df.to_csv(Path(curated_data_directory()) / 'session_filenames.csv')
    return df
