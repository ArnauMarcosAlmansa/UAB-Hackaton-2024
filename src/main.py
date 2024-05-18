from pprint import PrettyPrinter

import numpy as np

from src.data.data import load_from_xlsx, Town
from src.data.gmp import distance_matrix, distance_array

import dotenv

dotenv.load_dotenv()

if __name__ == '__main__':
    pp = PrettyPrinter(indent=4)
    ruta2, ruta4, ruta5 = load_from_xlsx("../data/Dades_Municipis.xlsx")

    # for ruta, towns in zip([2, 4, 5], [ruta2, ruta4, ruta5]):
    #     for b in range(1, 5):
    #         time_mat = distance_matrix([t for t in towns if t.block == b])
    #         np.save(f"../data/{ruta}_{b}.npy", time_mat)

    girona, barcelona, tarragona = [Town(batch=0, block=0, region="", ine_code="", name="Carrer Indústria, 0, 17457 Riudellots de la Selva, Girona", population=0,
                    min_stay_in_seconds=0),
               Town(batch=0, block=0, region="", ine_code="", name="Av les Garrigues, 9, 08820, El Prat de Llobregat", population=0,
                    min_stay_in_seconds=0),
               Town(batch=0, block=0, region="", ine_code="", name="Pol. Industrial Riu Clar C/Sofre, parcel·la 131 – nau 30 43006 Tarragona", population=0,
                    min_stay_in_seconds=0)]

    for city, origin in zip(["girona", "barcelona", "tarragona"], [girona, barcelona, tarragona]):
        for ruta, towns in zip([2, 4, 5], [ruta2, ruta4, ruta5]):
            for b in range(1, 5):
                time_array = distance_array(origin, [t for t in towns if t.block == b])
                np.save(f"../data/{city}_{ruta}_{b}.npy", time_array)

# pp.pprint(a)
