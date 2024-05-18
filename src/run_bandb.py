import pprint

import numpy as np

from src.algorithms.bandb import salesman_track_branch_and_bound
from src.algorithms.workday_splitting import workday_splitting
from src.data.data import load_from_xlsx
from src.utils import skip

ruta2, ruta4, ruta5 = load_from_xlsx("../data/Dades_Municipis.xlsx")

for origin_name, batch, ruta in zip(["tarragona", "girona", "barcelona"], [2, 4, 5], [ruta2, ruta4, ruta5]):
    for block in [1, 2, 3, 4]:
        distance_matrix = np.load(f"../data/{batch}_{block}.npy")
        origin_distances = np.load(f"../data/{origin_name}_{batch}_{block}.npy")

        print(f"LOTE = {batch}")
        print(f"ORIGEN = {origin_name}")
        print(f"BLOQUE = {block}")

        for dist, path in skip(10, salesman_track_branch_and_bound(distance_matrix)):
            splits = list(
                workday_splitting(path, distance_matrix, origin_distances, [t for t in ruta if t.block == block]))

            for split in splits:
                print(f"\tSPLIT = {split[1]}\tDURATION = {split[0]}")

            if sum(map(lambda s: s[0], splits)) > 60 * 60 * 39 or len(splits) > 5:
                print("MAL")
            else:
                print("BIEN")

            break
