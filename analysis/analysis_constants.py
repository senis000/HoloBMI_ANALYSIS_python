# constants to be used on analysis

from pathlib import Path
from os import listdir


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


def caiman_analysis_results_directory(aux_dir: Path) -> Path:
    return aux_dir / 'subvideo' / 'caiman_result'


def caiman_full_directory(aux_dir: Path, mice_name: str, date: str, day: str) -> Path:
    aux_bmi_directory = Path(aux_dir, mice_name + '_CaimanResults', date, mice_name, day, 'im', 'BMI')
    directory = listdir(aux_bmi_directory)
    if len(directory) == 1:
        return aux_bmi_directory / directory[0]
    else:
        raise FileNotFoundError(' The directory does not have a unique BMI_im result to check')


def voltage_rec_filename(aux_dir: Path) -> Path:
    files = [item for item in listdir(aux_dir) if item[-3:] == 'csv']
    if len(files) == 1:
        return aux_dir / files[0]
    else:
        raise FileNotFoundError(' The directory does not have a unique Voltage_rec result to check')


def caiman_analysis_file_path(aux_dir: Path) -> Path:
    return aux_dir / 'analysis_results.hdf5'


def motion_file_path(aux_dir: Path) -> Path:
    return aux_dir / 'mc_shifts.pkl'


def raw_folder(aux_dir: Path, mice_name: str, date: str, day: str) -> Path:
    aux_raw_directory = Path(aux_dir, date, mice_name, day, 'im', 'BMI')
    directory = listdir(aux_raw_directory)
    if len(directory) == 1:
        return aux_raw_directory / directory[0]
    else:
        raise FileNotFoundError(' The directory does not have a unique BMI_im result to check')


def raw_files(aux_dir: Path) -> list:
    directory = listdir(aux_dir)
    list_files = []
    for file in directory:
        if file[-3:] == 'tif' or file[-4:] == 'tiff':
            list_files.append(aux_dir/file)
    return list_files
