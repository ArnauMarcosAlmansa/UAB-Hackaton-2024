import numpy as np

from src.data.data import Town


def skip(n: int, iter):
    for i in range(n):
        try:
            next(iter)
        except StopIteration:
            return

    for elem in iter:
        yield elem


def seconds_to_time_str(seconds: int) -> str:
    secs = seconds % 60
    minutes = seconds // 60
    mins = minutes % 60
    hours = minutes // 60

    return f"{hours:02} h {mins:02} min {secs:02} s"


def print_path_split(split, towns: list[Town], origin: Town, distance_matrix: np.ndarray, origin_distances: np.ndarray):
    print(f"\t\t{origin.name}")
    print(f"\t\t>>> {seconds_to_time_str(origin_distances[split[1][0]])}")
    for part1, part2 in zip(split[1][0:-2], split[1][1:-1]):
        print(f"\t\t{towns[part1].name}, {towns[part1].region} --- {seconds_to_time_str(towns[part1].min_stay_in_seconds)}")
        print(f"\t\t>>> {seconds_to_time_str(distance_matrix[part1, part2])}")

    print(f"\t\t{towns[split[1][-1]].name}, {towns[split[1][-1]].region} --- {seconds_to_time_str(towns[split[1][-1]].min_stay_in_seconds)}")
    print(f"\t\t>>> {seconds_to_time_str(origin_distances[split[1][-1]])}")
    print(f"\t\t{origin.name}")
    print(f"\t\tTOTAL: {seconds_to_time_str(split[0])}")




def print_path_splits(splits, towns: list[Town], origin: Town, distance_matrix: np.ndarray, origin_distances: np.ndarray):
    for split in splits:
        print_path_split(split, towns, origin, distance_matrix, origin_distances)
        print()
