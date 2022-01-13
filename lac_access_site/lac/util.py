# LAC Access Site Utilities 
from django.conf import settings
from functools import reduce
import xml.etree.ElementTree as xml_parser
import requests

import pprint

# use http to fetch results from the partner site's rest api
def get_seeds(collection_id):
    endpoint = settings.API_ROOT + '/seed?collection=' + str(collection_id)
    auth_string = "Token " + settings.API_KEY
    headers = { "authorization":auth_string }

    #TODO handle http errors
    response = requests.get(endpoint, headers=headers)

    # parse api output
    seeds = []
    for seed in response.json():
        seed_info = {"url":seed["url"]}

        #TODO handle diff data structures
        for label, data in seed["metadata"].items():
            seed_info[label.lower()] = reduce(lambda accumulated_value, datum: accumulated_value + ' ' + datum["value"], data,'')
        seeds.append(seed_info)

    return seeds

def get_search_results(query,collection_ids=[]):
    endpoint = settings.SEARCH_ROOT 
    params = {"fmt":"json","q":query}

    if not collection_ids:
        # TODO derive from db models
        collection_ids = [6602,9155]
    params["i"]=collection_ids

    response = requests.get(endpoint, params=params)

    #xml_parser.fromstring(response.text)

    return response.json()
