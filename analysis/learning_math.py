# to analyze different learning stats.

import numpy as np
from typing import Tuple
import itertools


def time_to_hit(data: dict) -> Tuple[np.array, np.array]:
    """ returns time between hits """
    self_hits = data['selfHits']
    tth = list((sum(1 for _ in group) for value, group in itertools.groupby(self_hits) if value == 0))
    tth = np.asarray(tth)
    tth_array = np.zeros(self_hits.shape[0])
    hits_location = np.where(self_hits == 1)[0]
    for hh, hit in enumerate(hits_location):
        tth_array[hit] = tth[hh]
    return tth, tth_array
