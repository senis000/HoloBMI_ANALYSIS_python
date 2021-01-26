# class where to store/retrieve all the analysis results

import pandas as pd
from analysis.analysis_constants import *


class LearningResults:
    """ Class to retrieve all analysis results """

    def __init__(self, session_name: str):
        self._session_name = session_name

    def learning_behavior(self) -> pd.DataFrame:
        filename = learning_directory('') / learning_file_name(self._session_name)
        return pd.read_parquet(self._filename_mapper(filename))



