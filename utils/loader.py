# to load all results of one session

import datetime
import json
import logging
import os
import pickle
import pathlib
import posixpath
import re
import tempfile
from functools import lru_cache
from typing import Dict, Tuple, Optional, List

import numpy as np
import pandas as pd
import pendulum
from more_itertools import one
from analysis.analysis_constants import *
from analysis.analysis_results import LearningResults


def load_sessions() -> pd.DataFrame:
    local_dir_data = local_analysis_directory(AnalysisConstants.local_dir)
    df = pd.read_excel(sessions_path(local_dir_data), header=[0, 1], index_col=0)
    df.index = df.index.astype(str)
    return df


class SessionLoader(object):
    """
    Loads HoloBMI sessions. Loads from local files. Provides them as Pandas
    dataframes.

    """

    def __init__(self, session_date: str, mice_name: str):
        df_sessions = load_sessions()
        if mice_name in df_sessions:
            if session_date in df_sessions.index:
                self.session_date = session_date
                self.mice_name = mice_name
                self.session_name = obtain_session_name(mice_name, session_date)
                self.pretraining = df_sessions.loc[session_date, (mice_name, 'first')]
                self.training = df_sessions.loc[session_date, (mice_name, 'second')]
            else:
                raise ValueError('The date is not correct')
        else:
            raise ValueError('That name is not in our database')

    def learning(self) -> LearningResults:
        return LearningResults(session_name=self.session_date)