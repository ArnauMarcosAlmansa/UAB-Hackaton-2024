import os

import numpy as np
import requests

from src.data.data import Town


def distance_matrix(towns: list[Town]):
    town_names_query = "|".join(map(lambda t: t.name, towns))
    apikey = os.environ.get('GMP_API_KEY')

    time_matrix = np.zeros((len(towns), len(towns)))

    for i, origin in enumerate(towns):
        for j, destination in enumerate(towns):

            res = requests.get(
                "https://maps.googleapis.com/maps/api/distancematrix/json"
                f"?destinations={requests.utils.quote(destination.name + ', ' + destination.region)}"
                f"&origins={requests.utils.quote(origin.name + ', ' + origin.region)}"
                "&units=metric"
                f"&key={apikey}"
            )

            time_matrix[i, j] = res.json()["rows"][0]["elements"][0]["duration"]["value"]

    return time_matrix
