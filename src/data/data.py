import pandas as pd
from dataclasses import dataclass


@dataclass
class Town:
    batch: int
    block: int
    region: str
    ine_code: str
    name: str
    population: int
    min_stay_in_seconds: float


def convert_stay_to_minutes(stay: str):
    match stay:
        case "1 HORA":
            return 60.0 * 60.0
        case "30 MINUTOS":
            return 30.0 * 60.0
        case _:
            raise ValueError(f"Invalid stay: {stay}")


def convert_dataframe_to_towns(df: pd.DataFrame):
    batches = df['LOTE'].to_list()
    block = df['BLOC'].to_list()
    region = df['COMARCA'].to_list()
    ine_code = df['codINE'].to_list()
    name = df['Municipi'].to_list()
    population = df['Pob.'].to_list()
    min_stay = df['Estancia Minima'].to_list()
    min_stay_in_seconds = map(convert_stay_to_minutes, min_stay)

    iter = zip(batches, block, region, ine_code, name, population, min_stay_in_seconds)

    towns = []
    for batch, block, region, ine_code, name, population, min_stay_in_seconds in iter:
        towns.append(Town(batch=batch, block=block, region=region, ine_code=ine_code, name=name, population=population,
                          min_stay_in_seconds=min_stay_in_seconds))

    return towns


def load_from_xlsx(filename: str):
    xls = pd.ExcelFile(filename)

    df1 = pd.read_excel(xls, 'Ruta 2 ')
    df2 = pd.read_excel(xls, 'Ruta 4 ')
    df3 = pd.read_excel(xls, 'Ruta 5 ')

    return convert_dataframe_to_towns(df1), convert_dataframe_to_towns(df2), convert_dataframe_to_towns(df3)
