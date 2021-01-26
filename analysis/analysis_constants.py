# constants to be used on analysis

from pathlib import Path


def local_analysis_directory(aux_dir: Path) -> Path:
    return Path(aux_dir) / 'Analysis'


def plots_directory(aux_dir: Path) -> Path:
    return Path(aux_dir) / 'plots'


def learning_directory(aux_dir: Path) -> Path:
    return Path(aux_dir) / 'learning'


def learning_file_name(session_name: str) -> str:
    return f'{session_name}_learning_stats.parquet'


def path_learning_file_name(session_name: str, aux_dir: Path) -> Path:
    filename = learning_file_name(session_name)
    return Path(learning_directory(local_analysis_directory(aux_dir))) / filename
