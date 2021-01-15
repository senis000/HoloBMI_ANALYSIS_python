# constants to be used in general

import pandas as pd
from pathlib import Path
from dataclasses import dataclass


def cured_data_directory() -> Path:
    return GeneralConstants.local_dir / 'cured_data'


def sessions_path() -> Path:
    return cured_data_directory() / 'sessions.xlsx'


def raw_data_directory() -> Path:
    return GeneralConstants.local_dir / 'raw_data'


def obtain_session_name(session_date: str, mice_name: str) -> str:
    return mice_name + '_' + session_date


def files_directory(date: str, day: str, mice_name: str) -> Path:
    return raw_data_directory() / date / mice_name / day


def session_dataframe() -> pd.DataFrame:
    df = pd.read_excel(sessions_path(), header=[0, 1], index_col=0)
    df.index = df.index.astype(str)
    return df


@dataclass
class GeneralConstants:
    """  Class containing various constants for analysis, such as str for filenames """
    local_dir = Path("C:/Users/Nuria/Documents/DATA/holoBMI/")  # None
