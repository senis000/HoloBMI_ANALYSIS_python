# dataclass for analysis

import numpy as np
from pathlib import Path
from dataclasses import dataclass
from analysis.analysis_constants import *


def create_dirs():
    """ function to create the directories to store data or plots """
    local_dir_analysis = local_analysis_directory(AnalysisConfiguration.local_dir)
    if local_dir_analysis is not None:
        local_dir_learning = learning_directory(local_dir_analysis)
        if not local_dir_learning.exists():
            local_dir_learning.mkdir()
    if not local_dir_analysis.exists():
        local_dir_analysis.mkdir()
    if AnalysisConfiguration.to_plot:
        local_dir_plots = plots_directory(AnalysisConfiguration.local_dir)
        if not local_dir_plots.exists():
            local_dir_plots.mkdir()



@dataclass
class AnalysisConfiguration:
    """
    Class containing various configuration parameters for analysis. Reasonable defaults are
    provided.
    """

    # general
    tol = 0.05  # tolerance at which the pvalues will be consider significant

    # plotting
    to_plot: bool = True
