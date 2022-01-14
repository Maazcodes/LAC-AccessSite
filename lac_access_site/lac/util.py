# LAC Access Site Utilities 
from django.conf import settings
from functools import reduce
from time import sleep
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

def get_search_results(query,collection_ids="all", advanced=dict()):
    endpoint = settings.SEARCH_ROOT 
    params = {"fmt":"json","q":query}

    if collection_ids=="all":
        # TODO derive from db models
        collection_ids = [6602,9155]
    params["i"]=collection_ids

    # handle params from the advanced search interface
    # TODO can maybe reduce these
    for param_name,value in advanced.items():
        if param_name=='nq' and value != '':
            params["q"]=query+' -'+value
        if param_name=='exact' and value != '':
            params["q"]=query+' \"'+value+'\"'
        if param_name=='site' and value != '':
            params["s"]=value
        if param_name=='filetype' and value != '':
            params["t"]=value
        if param_name=='start' and value != '':
            params["start_date"]=value
        if param_name=='end' and value != '':
            params["end_date"]=value

    pprint.pprint(params)
    response = requests.get(endpoint, params=params)
    
    # fix 'decode error' ie check for no result, try again 
    if not response.ok:
        sleep(1)
        response = requests.get(endpoint, params=params)

    pprint.pprint(response.json())
    #pprint.pprint(response.text())


    return response.json()
