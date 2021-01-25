# to load all results of one session

import pandas as pd
from utils.general_constants import *
from analysis.analysis_constants import *
from analysis.analysis_results import LearningResults
from utils.utils_loader import from_matlab_file_to_dict


def load_sessions() -> pd.DataFrame:
    df = pd.read_excel(sessions_path(), header=[0, 1], index_col=0)
    df.index = df.index.astype(str)
    return df


def load_sessions_filename() -> pd.DataFrame:
    df = pd.read_parquet(sessions_filenames())
    return df


class SessionLoader(object):
    """
    Loads HoloBMI sessions. Loads from local files. Provides them as Pandas
    dataframes.

    """

    def __init__(self, session_date: str, mice_name: str):
        df_sessions = load_sessions_filename()
        if mice_name in df_sessions:
            if session_date in df_sessions.index:
                self.session_date = session_date
                self.mice_name = mice_name
                self.session_name = obtain_session_name(mice_name, session_date)
                self.pretraining = df_sessions.loc[session_date, (mice_name, '1_exp')]
                self.training = df_sessions.loc[session_date, (mice_name, '2_exp')]
                aux_day = df_sessions.loc[session_date, 'Day']
                self.day = aux_day[aux_day.notna()].values[0]
                self.file_baseline = df_sessions.loc[session_date, (mice_name, 'file_baseline')]
                self.file_holostim = df_sessions.loc[session_date, (mice_name, 'file_holostim')]
                self.file_pretraining = df_sessions.loc[session_date, (mice_name, 'file_pretraining')]
                self.file_training = df_sessions.loc[session_date, (mice_name, 'file_training')]
                self.file_target_cal = df_sessions.loc[session_date, (mice_name, 'file_target_cal')]
                self.file_target_info = df_sessions.loc[session_date, (mice_name, 'file_target_info')]
            else:
                raise ValueError('The date is not correct')
        else:
            raise ValueError('That name is not in our database')

    def learning(self) -> LearningResults:
        return LearningResults(session_name=self.session_date)

    def results_baseline_dict(self) -> dict:
        return from_matlab_file_to_dict(files_directory(self.session_date, self.day, self.mice_name)/self.file_baseline)

    def results_holostim_dict(self) -> dict:
        return from_matlab_file_to_dict(files_directory(self.session_date, self.day, self.mice_name)/self.file_holostim)

    def results_pretraining_dict(self) -> dict:
        return from_matlab_file_to_dict(files_directory(self.session_date, self.day, self.mice_name)/self.file_pretraining)

    def results_training_dict(self) -> dict:
        return from_matlab_file_to_dict(files_directory(self.session_date, self.day, self.mice_name)/self.file_training)

    def results_target_calibration_dict(self) -> dict:
        return from_matlab_file_to_dict(files_directory(self.session_date, self.day, self.mice_name)/self.file_target_cal)

    def results_target_info_dict(self) -> dict:
        return from_matlab_file_to_dict(files_directory(self.session_date, self.day, self.mice_name)/self.file_target_info)



