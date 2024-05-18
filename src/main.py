from pprint import PrettyPrinter

from src.data.data import load_from_xlsx

if __name__ == '__main__':
    pp = PrettyPrinter(indent=4)
    a, b, c = load_from_xlsx("data/Dades_Municipis.xlsx")
    pp.pprint(a)