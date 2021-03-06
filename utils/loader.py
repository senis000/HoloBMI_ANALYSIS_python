# to load all results of one session
import pandas as pd
import numpy as np
from typing import Tuple

from utils.general_constants import sessions_path, sessions_filenames, obtain_session_name, occupancy_path, \
    occupancy_t2_path, hits_t2_path, hits_path, occupancy_baseline_path, occupancy_baseline_t2_path
from analysis.analysis_results import LearningResults
from utils.utils_loader import load_dict


def load_sessions() -> pd.DataFrame:
    df = pd.read_excel(sessions_path(), header=[0, 1], index_col=0)
    df.index = df.index.astype(str)
    return df


def load_sessions_filename() -> pd.DataFrame:
    df = pd.read_parquet(sessions_filenames())
    return df


def load_occupancy() -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    df = pd.read_parquet(occupancy_path())
    df = df.set_index('rows')
    df.index = df.index.astype(str)
    df_2 = pd.read_parquet(occupancy_t2_path())
    df_2 = df_2.set_index('rows')
    df_2.index = df_2.index.astype(str)
    df_b = pd.read_parquet(occupancy_baseline_path())
    df_b = df_b.set_index('rows')
    df_b.index = df_b.index.astype(str)
    df_b2 = pd.read_parquet(occupancy_baseline_t2_path())
    df_b2 = df_b2.set_index('rows')
    df_b2.index = df_b2.index.astype(str)
    return df, df_2, df_b, df_b2


def load_hits() -> Tuple[pd.DataFrame, pd.DataFrame]:
    df = pd.read_parquet(hits_path())
    df = df.set_index('rows')
    df.index = df.index.astype(str)
    df_2 = pd.read_parquet(hits_t2_path())
    df_2 = df_2.set_index('rows')
    df_2.index = df_2.index.astype(str)
    return df, df_2


def load_names_dates() -> Tuple[pd.core.indexes.base.Index, pd.core.indexes.base.Index, np.array, np.array]:
    df_sessions = load_sessions_filename()
    dates = df_sessions.index
    mice_names = df_sessions.columns.levels[0][1:]
    type_pre_trainings = np.unique(np.concatenate(df_sessions.loc[slice(None), (slice(None), '1_exp')].values).astype(str))
    type_pre_trainings = type_pre_trainings[type_pre_trainings != 'None']
    type_trainings = np.unique(np.concatenate(df_sessions.loc[slice(None), (slice(None), '2_exp')].values).astype(str))
    type_trainings = type_trainings[type_trainings != 'None']
    return mice_names, dates, type_pre_trainings, type_trainings


class FileNames:
    def __init__(self, df_sessions: pd.DataFrame, session_date: str, mice_name: str):
        self.file_baseline = df_sessions.loc[session_date, (mice_name, 'file_baseline')]
        self.file_holostim = df_sessions.loc[session_date, (mice_name, 'file_holostim')]
        self.file_pretraining = df_sessions.loc[session_date, (mice_name, 'file_pretraining')]
        self.file_training = df_sessions.loc[session_date, (mice_name, 'file_training')]
        self.file_target_cal = df_sessions.loc[session_date, (mice_name, 'file_target_cal')]
        self.file_target_info = df_sessions.loc[session_date, (mice_name, 'file_target_info')]
        self.file_strc_mask = 'strcMask.mat'


class ExperimentVariables:
    def __init__(self, df_sessions: pd.DataFrame, session_date: str, mice_name: str, day: str):
        self._session_date = session_date
        self._mice_name = mice_name
        self._day = day
        self.file_names = FileNames(df_sessions, session_date, mice_name)

    def dict_baseline(self) -> dict:
        return load_dict(self._session_date, self._day, self._mice_name, self.file_names.file_baseline)

    def dict_holostim(self) -> dict:
        return load_dict(self._session_date, self._day, self._mice_name, self.file_names.file_holostim)

    def dict_pretraining(self) -> dict:
        return load_dict(self._session_date, self._day, self._mice_name, self.file_names.file_pretraining)

    def dict_training(self) -> dict:
        return load_dict(self._session_date, self._day, self._mice_name, self.file_names.file_training)

    def dict_target_calibration(self) -> dict:
        return load_dict(self._session_date, self._day, self._mice_name, self.file_names.file_target_cal)

    def dict_target_info(self) -> dict:
        return load_dict(self._session_date, self._day, self._mice_name, self.file_names.file_target_info)

    def dict_strc_mask(self) -> dict:
        return load_dict(self._session_date, self._day, self._mice_name, self.file_names.file_strc_mask)

    def dict_task_settings(self) -> dict:
        workspace = load_dict(self._session_date, self._day, self._mice_name, 'workspace.mat')
        return workspace['task_settings']

    def array_hits(self) -> np.array:
        training_dict = self.dict_training()
        array_hits = training_dict['data']['selfHits']
        last_frame = training_dict['data']['frame']
        array_hits = array_hits[:last_frame - 1]
        return array_hits.astype(int)


class SessionLoader(object):
    """
    Loads HoloBMI sessions and results of analysis. Loads from local files.

    """

    def __init__(self, session_date: str, mice_name: str):
        self._df_sessions = load_sessions_filename()
        if mice_name in self._df_sessions:
            if session_date in self._df_sessions.index:
                self.session_date = session_date
                self.mice_name = mice_name
                self.session_name = obtain_session_name(mice_name, session_date)
                self.pretraining_type = self._df_sessions.loc[session_date, (mice_name, '1_exp')]
                self.training_type = self._df_sessions.loc[session_date, (mice_name, '2_exp')]
                aux_day = self._df_sessions.loc[session_date, 'Day']
                self.day = aux_day[aux_day.notna()].values[0]
                self.experiment_variables = \
                    ExperimentVariables(self._df_sessions, self.session_date, self.mice_name, self.day)
                try:
                    self.learning = LearningResults(session_name=self.session_name)
                except FileNotFoundError:
                    self.learning = 'no learning analyzed yet'
            else:
                raise ValueError('The date is not correct')
        else:
            raise ValueError('That name is not in our database')


