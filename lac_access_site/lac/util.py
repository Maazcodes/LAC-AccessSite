# LAC Access Site Utilities 
from django.conf import settings
import requests

import pprint
from functools import reduce

# use http to fetch results from the partner site's api
def get_seeds(collection_id):
    # pull dynamically from ait http api
    endpoint = settings.API_ROOT + '/seed?collection=' + str(collection_id)
    auth_string = "Token " + settings.API_KEY
    headers = { "authorization":auth_string }

    response = requests.get(endpoint, headers=headers)

    # parse api output
    seeds = []
    for seed in response.json():
        seed_info = {"url":seed["url"]}
        for label, data in seed["metadata"].items():
            seed_info[label.lower()] = reduce(lambda accumulated_value, datum: accumulated_value + ' ' + datum["value"], data,'')
        seeds.append(seed_info)

    pprint.pprint(seeds)

    return seeds

