import numpy as np

from src.data.data import Town


def workday_splitting(path: list[int], distance_matrix: np.ndarray, origin_distances: np.ndarray, towns: list[Town]):
    time_spent = 0
    last_pos = path[0]
    time_spent += origin_distances[last_pos]
    time_spent += towns[last_pos].min_stay_in_seconds

    path_split = []

    for p in path[1:]:
        if time_spent + distance_matrix[last_pos, p] + towns[p].min_stay_in_seconds + origin_distances[p] > 60 * 60 * 8:
            yield time_spent, path_split
            path_split = []
            time_spent = 0

        time_spent += distance_matrix[last_pos, p]
        last_pos = p
        time_spent += towns[p].min_stay_in_seconds
        path_split.append(p)
