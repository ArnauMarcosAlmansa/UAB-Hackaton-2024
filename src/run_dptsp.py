import pprint

from python_tsp.exact import solve_tsp_dynamic_programming
import numpy as np

distance_matrix = np.load("../data/2_1.npy")

permutation, distance = solve_tsp_dynamic_programming(distance_matrix)

pprint.pprint(permutation)