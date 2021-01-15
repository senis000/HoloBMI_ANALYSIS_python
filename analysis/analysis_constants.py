# constants to be used on analysis (similar to airflow_dags constants but for offline processing)

from pathlib import Path
from dataclasses import dataclass


def local_analysis_directory(aux_dir: Path) -> Path:
    return aux_dir / 'Analysis'


def cured_data_directory(aux_dir: Path) -> Path:
    return aux_dir / 'cured_data'


def sessions_path(aux_dir: Path) -> Path:
    return aux_dir / 'sessions.xlsx'


def obtain_session_name(session_date: str, mice_name: str) -> str:
    return mice_name + '_' + session_date


def plots_directory(aux_dir: Path) -> Path:
    return aux_dir / 'plots'


def learning_directory(aux_dir: Path) -> Path:
    return aux_dir / 'learning'


def learning_file_name(session_name: str) -> str:
    return f'{session_name}_learning_stats.parquet'





@dataclass
class AnalysisConstants:
    """  Class containing various constants for analysis, such as str for filenames """
    local_dir = Path("C:/Users/Nuria/Documents/DATA/holoBMI/")  # None