from pprint import PrettyPrinter

import numpy as np

from src.data.data import load_from_xlsx, Town
from src.data.gmp import distance_matrix, distance_array, coords

import dotenv

dotenv.load_dotenv()

if __name__ == '__main__':
    pp = PrettyPrinter(indent=4)
    ruta2, ruta4, ruta5 = load_from_xlsx("../data/Dades_Municipis.xlsx")

    for block in [1, 2, 3, 4]:
        coords2 = coords([t for t in ruta2 if t.block == block])
        coords4 = coords([t for t in ruta4 if t.block == block])
        coords5 = coords([t for t in ruta5 if t.block == block])

        np.save(f"coords_2_{block}.npy", coords2)
        np.save(f"coords_4_{block}.npy", coords4)
        np.save(f"coords_5_{block}.npy", coords5)

