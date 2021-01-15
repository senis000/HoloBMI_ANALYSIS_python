# to analyze different learning stats.

import numpy as np
from typing import Tuple
import itertools


def time_to_hit(array_hits: np.array) -> Tuple[np.array, np.array]:
    """ returns time between hits """
    tth = list((sum(1 for _ in group) for value, group in itertools.groupby(array_hits) if value == 0))
    tth = np.asarray(tth)
    tth_array = np.zeros(array_hits.shape[0])
    hits_location = np.where(array_hits == 1)[0]
    for hh, hit in enumerate(hits_location):
        tth_array[hit] = tth[hh]
    return tth, tth_array
