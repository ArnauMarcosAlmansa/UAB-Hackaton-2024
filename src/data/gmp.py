import os

import requests

from src.data.data import Town


def distance_matrix(towns: list[Town]):
    towns = "|".join(map(lambda t: t.name, towns))

    print(towns)

    apikey = os.environ.get('GMP_API_KEY')

    res = requests.get(
        "https://maps.googleapis.com/maps/api/distancematrix/json"
        f"?destinations={requests.utils.quote(towns)}"
        f"&origins={requests.utils.quote(towns)}"
        "&units=metric"
        f"&key={apikey}"
    )

    print(res.text)
