# constants to be used on analysis

from pathlib import Path
from dataclasses import dataclass


def local_analysis_directory(aux_dir: Path) -> Path:
    return aux_dir / 'Analysis'


def plots_directory(aux_dir: Path) -> Path:
    return aux_dir / 'plots'


def learning_directory(aux_dir: Path) -> Path:
    return aux_dir / 'learning'


def learning_file_name(session_name: str) -> str:
    return f'{session_name}_learning_stats.parquet'