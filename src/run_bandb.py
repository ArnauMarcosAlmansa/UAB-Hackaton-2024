import pprint

import dotenv
import numpy as np

from src.algorithms.bandb import salesman_track_branch_and_bound
from src.algorithms.workday_splitting import workday_splitting
from src.data.data import load_from_xlsx, Town
from src.utils import skip, print_path_splits, get_workdays_of_month, split_into_packs, display_path_splits
from src.data.gmp import coords

dotenv.load_dotenv()

ruta2, ruta4, ruta5 = load_from_xlsx("../data/Dades_Municipis.xlsx")

girona, barcelona, tarragona = [
                Town(batch=0, block=0, region="", ine_code="", name="Carrer Indústria, 0, 17457 Riudellots de la Selva, Girona", population=0,
                    min_stay_in_seconds=0),
                Town(batch=0, block=0, region="", ine_code="", name="Av les Garrigues, 9, 08820, El Prat de Llobregat", population=0,
                    min_stay_in_seconds=0),
                Town(batch=0, block=0, region="", ine_code="", name="Pol. Industrial Riu Clar C/Sofre, parcel·la 131 – nau 30 43006 Tarragona", population=0,
                    min_stay_in_seconds=0)]

cds = coords([girona, barcelona, tarragona])
girona.lat = cds[0, 0]
girona.lon = cds[0, 1]
barcelona.lat = cds[1, 0]
barcelona.lon = cds[1, 1]
tarragona.lat = cds[2, 0]
tarragona.lon = cds[2, 1]

bases = {"tarragona": tarragona, "girona": girona, "barcelona": barcelona}

workdays_of_month = get_workdays_of_month(2024, 9)[:20]
workdays_per_block = split_into_packs(workdays_of_month)

for origin_name, batch, ruta in zip(["tarragona", "girona", "barcelona"], [2, 4, 5], [ruta2, ruta4, ruta5]):
    for block, workdays in zip([1, 2, 3, 4], workdays_per_block):
        distance_matrix = np.load(f"../data/{batch}_{block}.npy")
        origin_distances = np.load(f"../data/{origin_name}_{batch}_{block}.npy")
        coords = np.load(f"../data/coords_{batch}_{block}.npy")

        print(f"LOTE = {batch}")
        print(f"ORIGEN = {origin_name}")
        print(f"BLOQUE = {block}")

        for dist, path in skip(20, salesman_track_branch_and_bound(distance_matrix)):
            towns = [t for t in ruta if t.block == block]
            splits = list(
                workday_splitting(workdays, path, distance_matrix, origin_distances, towns))

            for split in splits:
                print(f"\tSPLIT = {split[1]}\tDURATION = {split[0]}")

            print("\tPATH:")

            print_path_splits(splits, towns, bases[origin_name], distance_matrix, origin_distances)

            display_path_splits(batch, block, splits, towns, bases[origin_name], coords)

            if sum(map(lambda s: s[0], splits)) > 60 * 60 * 39 or len(splits) > 5:
                print("MAL")
            else:
                print("BIEN")

            break
