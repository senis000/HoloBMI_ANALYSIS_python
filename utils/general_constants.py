# constants to be used in general

from pathlib import Path
from dataclasses import dataclass


def curated_data_directory() -> Path:
    return GeneralConstants.local_dir / 'curated_data'


def sessions_path() -> Path:
    return curated_data_directory() / 'sessions.xlsx'


def sessions_filenames() -> Path:
    return curated_data_directory() / 'session_filenames.parquet'


def raw_data_directory() -> Path:
    return GeneralConstants.local_dir / 'raw_data'


def obtain_session_name(session_date: str, mice_name: str) -> str:
    return mice_name + '_' + session_date


def files_directory(date: str, day: str, mice_name: str) -> Path:
    return raw_data_directory() / date / mice_name / day




@dataclass
class GeneralConstants:
    """  Class containing various constants for analysis, such as str for filenames """
    local_dir = Path("C:/Users/Nuria/Documents/DATA/holoBMI/")  # None
    frame_rate = 30
