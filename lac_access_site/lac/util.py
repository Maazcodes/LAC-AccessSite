# LAC Access Site Utilities 
from django.conf import settings
import requests
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

import http

from pprint import pprint

def http_get_with_retries(endpoint, num_retries=4, **kwargs):
    retry_strategy = Retry(total=num_retries, backoff_factor=3, status_forcelist=[429, 500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retry_strategy)
    http_session = requests.Session()
    http_session.mount('https://', adapter)

    #debugging
    if settings.DEBUG:
        print("Sending http request")
        http.client.HTTPConnection.debuglevel = 1

    return http_session.get(endpoint, **kwargs)


# use http to fetch results from the partner site's rest api
def get_seeds(collection_ids):
    seeds = []
    topics = set()

    for ait_collection_id in collection_ids:
        endpoint = settings.API_ROOT + 'seed'
        
        auth_string = "Token " + settings.API_KEY
        
        headers = { "authorization":auth_string }
        
        params = { "collection":str(ait_collection_id),
                   "limit":str(-1),
                   "publicly_visible":True}

        #TODO handle http errors - like invalid token!
        response = http_get_with_retries(endpoint, headers=headers, params=params)
        
        # parse api output into a nicer structure for the template
        for seed in response.json():
            seed_info = {"url":seed["url"]}
            for label, data in seed["metadata"].items():
                if label.lower() == 'subject':
                    seed_info[label.lower()] = [datum['value'] for datum in data]
                    topics.update(seed_info[label.lower()])
                else:
                    seed_info[label.lower()] = data[0]['value']
            
            seeds.append(seed_info)
        
    return {'data':seeds, 'topics':topics}

def get_search_results(query,collection_ids, advanced=dict()):
    endpoint = settings.SEARCH_ROOT 
    params = {"fmt":"json","q":query}

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

    response = http_get_with_retries(endpoint, params=params)

    #undo some escaping from the search endpoint
    results = []
    response_items = response.json()['items']
    for item in response_items:
        item['description']=item['description'].replace('&lt;b&gt;','<b>').replace('&lt;/b&gt;','</b>')
        results.append(item)

    return results
