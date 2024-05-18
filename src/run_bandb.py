import pprint

import numpy as np

from src.algorithms.bandb import salesman_track_branch_and_bound

distance_matrix = np.load("../data/2_1.npy")

for dist, path in salesman_track_branch_and_bound(distance_matrix[0:20, 0:20]):
    pprint.pprint(f"{dist}, {path}")
