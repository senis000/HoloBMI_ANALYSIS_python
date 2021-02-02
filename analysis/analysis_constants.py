# constants to be used on analysis

from pathlib import Path


def local_analysis_directory(aux_dir: Path) -> Path:
    return Path(aux_dir) / 'Analysis'


def plots_directory(aux_dir: Path) -> Path:
    return Path(aux_dir) / 'plots'


def population_directory(aux_dir: Path) -> Path:
    return Path(aux_dir) / 'population'


def learning_directory(aux_dir: Path) -> Path:
    return Path(aux_dir) / 'learning'


def learning_stats_file_name(session_name: str) -> str:
    return f'{session_name}_learning_stats.parquet'


def path_learning_stats_file_name(session_name: str, aux_dir: Path) -> Path:
    filename = learning_stats_file_name(session_name)
    return Path(learning_directory(local_analysis_directory(aux_dir))) / 'learning_per_mice' /filename


def learning_curve_file_name(session_name: str) -> str:
    return f'{session_name}_learning_curve.parquet'


def path_learning_curve_file_name(session_name: str, aux_dir: Path) -> Path:
    filename = learning_curve_file_name(session_name)
    return Path(learning_directory(local_analysis_directory(aux_dir))) / 'learning_per_mice' / filename


def learning_all_occupancy_path(aux_dir, n_exp) -> Path:
    filename = 'learning_occupancy_' + n_exp + '.parquet'
    return learning_directory(local_analysis_directory(aux_dir)) / filename


def learning_all_stats_path(aux_dir, n_exp) -> Path:
    filename = 'learning_stats_' + n_exp + '.parquet'
    return learning_directory(local_analysis_directory(aux_dir)) / filename


def learning_all_curves_path(aux_dir, n_exp) -> Path:
    filename = 'learning_curve_' + n_exp + '.parquet'
    return learning_directory(local_analysis_directory(aux_dir)) / filename
