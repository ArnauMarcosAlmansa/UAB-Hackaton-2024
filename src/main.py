from pprint import PrettyPrinter

import numpy as np

from src.data.data import load_from_xlsx
from src.data.gmp import distance_matrix

import dotenv

dotenv.load_dotenv()

if __name__ == '__main__':
    pp = PrettyPrinter(indent=4)
    ruta2, ruta4, ruta5 = load_from_xlsx("../data/Dades_Municipis.xlsx")

    for ruta, towns in zip([2, 4, 5], [ruta2, ruta4, ruta5]):
        for b in range(1, 5):
            time_mat = distance_matrix([t for t in towns if t.block == b])
            np.save(f"../data/{ruta}_{b}.npy", time_mat)

    # pp.pprint(a)