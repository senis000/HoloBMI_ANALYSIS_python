# dataclass for analysis

import numpy as np
from pathlib import Path
from dataclasses import dataclass
from analysis.analysis_constants import learning_directory


def create_dirs():
    """ function to create the directories to store data or plots """

    if not AnalysisConfiguration.local_dir.exists():
        AnalysisConfiguration.local_dir.mkdir()
    if not AnalysisConfiguration.plot_path.exists():
        AnalysisConfiguration.plot_path.mkdir()
    if AnalysisConfiguration.local_dir is not None:
        local_dir_learning = learning_directory(AnalysisConfiguration.local_dir)
        if not local_dir_learning.exists():
            local_dir_learning.mkdir()


@dataclass
class AnalysisConfiguration:
    """
    Class containing various configuration parameters for analysis. Reasonable defaults are
    provided.
    """

    # dirs
    local_dir = Path("C:/Users/Nuria/Documents/DATA/Analysis/")  # None

    # general
    tol = 0.05  # tolerance at which the pvalues will be consider significant

    # plotting
    to_plot: bool = True
    plot_path = Path("C:/Users/Nuria/DATA/plots")
