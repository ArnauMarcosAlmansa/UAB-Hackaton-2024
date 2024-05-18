from pprint import PrettyPrinter

from src.data.data import load_from_xlsx
from src.data.gmp import distance_matrix

import dotenv

dotenv.load_dotenv()

if __name__ == '__main__':
    pp = PrettyPrinter(indent=4)
    a, b, c = load_from_xlsx("data/Dades_Municipis.xlsx")

    distance_matrix([t for t in a if t.block == 1])
    # pp.pprint(a)