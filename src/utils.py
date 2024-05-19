import calendar
import time
import webbrowser
from datetime import date, datetime

import numpy as np
import pandas as pd

from src.data.data import Town
import folium
from IPython.display import display
from itertools import pairwise


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
        print(
            f"\t\t{towns[part1].name}, {towns[part1].region} --- {seconds_to_time_str(towns[part1].min_stay_in_seconds)}")
        print(f"\t\t>>> {seconds_to_time_str(distance_matrix[part1, part2])}")

    print(
        f"\t\t{towns[split[1][-1]].name}, {towns[split[1][-1]].region} --- {seconds_to_time_str(towns[split[1][-1]].min_stay_in_seconds)}")
    print(f"\t\t>>> {seconds_to_time_str(origin_distances[split[1][-1]])}")
    print(f"\t\t{origin.name}")
    print(f"\t\tTOTAL: {seconds_to_time_str(split[0])}")


def print_path_splits(splits, towns: list[Town], origin: Town, distance_matrix: np.ndarray,
                      origin_distances: np.ndarray):
    for split in splits:
        print_path_split(split, towns, origin, distance_matrix, origin_distances)
        print()


def get_workdays_of_month(year: int, month: int) -> list[date]:
    # Get the number of days in the given month
    num_days = calendar.monthrange(year, month)[1]
    # Create a date range for the month
    date_range = pd.date_range(start=f'{year}-{month:02d}-01', end=f'{year}-{month:02d}-{num_days}')
    # Filter out the business days
    business_days = date_range[date_range.dayofweek < 5]
    # Convert to list of strings in YYYY-MM-DD format
    business_days_list = business_days.strftime('%Y-%m-%d').tolist()

    return [datetime.strptime(str_date, "%Y-%m-%d")
            for str_date in business_days_list]


def split_into_packs(business_days, pack_size=5):
    return [business_days[i:i + pack_size] for i in range(0, len(business_days), pack_size)]

def display_path_splits(batch: int, block: int, splits, towns: list[Town], origin: Town, coords: np.ndarray):
    avg_location = coords.mean(0)

    for i, town in enumerate(towns):
        town.lat = coords[i, 0]
        town.lon = coords[i, 1]

    for i, split in enumerate(splits):
        map_route = folium.Map(location=avg_location, zoom_start=13)
        path = [origin]
        for p in split[1]:
            path.append(towns[p])
        path.append(origin)

        for j, town in enumerate(path[:-1]):
            marker = folium.Marker(location=(town.lat, town.lon),
                                   tooltip=town.name, icon=folium.Icon(color="blue" if j > 0 else "red"))
            marker.add_to(map_route)

        for town1, town2 in pairwise(path):
            line = folium.PolyLine(
                locations=[(town1.lat, town1.lon),
                           (town2.lat, town2.lon)],
                tooltip=f"De {town1.name} a {town2.name}",
            )
            line.add_to(map_route)

        map_route.save(f"map_{batch}_{block}_{i}.html")
        webbrowser.open(f"map_{batch}_{block}_{i}.html")

        time.sleep(1)
