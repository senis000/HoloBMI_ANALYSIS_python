# constants to be used on analysis (similar to airflow_dags constants but for offline processing)

from pathlib import Path
from dataclasses import dataclass


def local_directory(aux_dir: Path, session_name: str) -> Path:
    return aux_dir / session_name


def learning_directory(aux_dir: Path) -> Path:
    return aux_dir / "learning"


def analysis_configuration_file(session_name: str) -> str:
    return f'{session_name}_analysis_configuration.pkl'


@dataclass
class AnalysisConstants:
    """  Class containing various constants for analysis, such as str for filenames """
    var_error = 'error'