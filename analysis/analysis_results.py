# class where to store/retrieve all the analysis results

import pandas as pd

from analysis.analysis_constants import path_learning_stats_file_name, path_learning_curve_file_name
from utils.general_constants import GeneralConstants


class LearningResults:
    """ Class to retrieve all analysis results """

    def __init__(self, session_name: str):
        self._session_name = session_name
        self.learning_stats = \
            pd.read_parquet(path_learning_stats_file_name(self._session_name, GeneralConstants.local_dir))
        self.learning_curves = \
            pd.read_parquet(path_learning_curve_file_name(self._session_name, GeneralConstants.local_dir))




