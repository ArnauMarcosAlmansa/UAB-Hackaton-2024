import os

import numpy as np
import requests

from src.data.data import Town


def distance(origin: str, destination: str) -> float:
    apikey = os.environ.get('GMP_API_KEY')

    res = requests.get(
        "https://maps.googleapis.com/maps/api/distancematrix/json"
        f"?destinations={requests.utils.quote(destination)}"
        f"&origins={requests.utils.quote(origin)}"
        "&units=metric"
        f"&key={apikey}"
    )

    return res.json()["rows"][0]["elements"][0]["duration"]["value"]


def distance_matrix(towns: list[Town]):
    time_matrix = np.zeros((len(towns), len(towns)))

    for i, origin in enumerate(towns):
        for j, destination in enumerate(towns):
            time_matrix[i, j] = distance(origin.name + ', ' + origin.region,
                                         destination.name + ', ' + destination.region)

    return time_matrix


def distance_array(origin: Town, towns: list[Town]):
    time_array = np.zeros(len(towns))

    for i, destination in enumerate(towns):
        time_array[i] = distance(origin.name,
                                 destination.name + ', ' + destination.region)

    return time_array
