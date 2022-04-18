# LAC Access Site Utilities 
from cgitb import reset
import re
from urllib import response
from django.conf import settings
from django.core.paginator import Paginator
import requests
from datetime import date
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
                if label.lower() == 'subject' or label.lower() == 'sujet':
                    seed_info[label.lower()] = [datum['value'] for datum in data]
                    topics.update(seed_info[label.lower()])
                else:
                    seed_info[label.lower()] = data[0]['value']
            
            seeds.append(seed_info)
        
        #TODO remove debug
        #pprint(seeds)
        
    return {'data':seeds, 'topics':topics}

def get_days_in_month(date):
    if date.month==2:
        if (date.year % 400) == 0:
            return 29;
        elif (date.year % 100) == 0:
            return 28;
        elif (date.year % 4) == 0:
            return 29;
    elif date.month in [1,3,5,7,8,60,12]:
        return 31;
    else:
        return 30;

def get_date_range(start=date(1991,8,6), end=date.today()):
    
    if start < date(1991,8,6):
        start = date(1991,8,6) #year of the first webpage
    if end < date(1991,8,7):
        end = date(1991,8,7) 

    # generate date prefixes for the indicated time interval
    days = [start.replace(day=x).strftime("%Y%m%d") for x in range(start.day, get_days_in_month(start)+1) ] + [end.replace(day=x).strftime("%Y%m%d") for x in range(1, end.day+1) ]
    months = [start.replace(month=x).strftime("%Y%m") for x in range(start.month+1, 13) ] + [end.replace(month=x).strftime("%Y%m") for x in range(1, end.month) ]
    years = [str(start.year + x) for x in range(1, (end.year-start.year))]

    interval = days + months + years
    pprint(interval)
    return interval


def get_search_results(query,collection_ids, request):
    PER_PAGE_DEFAULT = 30
    endpoint = settings.SEARCH_ROOT 
    params = {"fmt":"json","q":query }

    params["i"]=collection_ids

    get_query_params = request.GET

    params["n"] = PER_PAGE_DEFAULT
        
    page = get_query_params.get("page", "1")
    if page.isdigit() and int(page) > 1:
        params['p'] = (int(page) - 1) * int(PER_PAGE_DEFAULT)

    # handle params from the advanced search interface
    # TODO can maybe reduce these
    for param_name,value in get_query_params.items():
        if param_name=='nq' and value != '':
            params["q"]=query+' -'+value
        if param_name=='exact' and value != '':
            params["q"]=query+' \"'+value+'\"'
        if param_name=='site' and value != '':
            params["s"]=value
        if param_name=='filetype' and value != '':
            params["t"]=value
    
    #handle date range
    if "start" in get_query_params and get_query_params.get('start','') != '':
        if "end" in get_query_params and get_query_params.get('end','') != '':
            params["d"]=get_date_range(start=date.fromisoformat(get_query_params["start"]), end=date.fromisoformat(get_query_params["end"]))
        else:
            params["d"]=get_date_range(start=date.fromisoformat(get_query_params["start"]))
    elif "end" in get_query_params and get_query_params.get('end','') != '':
        params["d"]=get_date_range(end=date.fromisoformat(get_query_params["end"]))

    response = http_get_with_retries(endpoint, params=params) 
    results = AitOpensearchResult(response.json(), params['n'], request.headers.get('X-Requesting-Page', ""))
    return results



class AitOpensearchResult:
    def __init__(self, response, per_page, requesting_url):
        self.requesting_url = requesting_url 
        self.response = response
        self.count = response['totalResults']
        self.per_page = per_page
        self.start = response['startIndex']
        self.current_page = (self.start // self.per_page) +1 
        self.num_pages = (self.count // self.per_page) +1

    def results(self):
        return [
            {**item, 'description': item['description'].replace('&lt;b&gt;','<b>').replace('&lt;/b&gt;','</b>')} 
            for item in self.response['items']
        ]


    def has_next_page(self):
        return self.current_page < self.num_pages
    
    def next_page(self):
        return self.page(self.current_page + 1)

    def has_prev_page(self):
        return self.current_page > 1

    def prev_page(self):
        return self.page(self.current_page - 1)
    
    def first_page(self):
        return self.page(1)
    
    def last_page(self):
        return self.page(self.num_pages)

    def page(self, page_number: int):
        if page_number < 1:
            page_number = 1
        if page_number > self.num_pages:
            page_number = self.num_pages
        return self.set_page_number_for_link(page_number)
    
    def page_range(self):
        empty_link = [{"n":"...", "link": ""}]
        if self.num_pages == 1:
            return []
        if self.num_pages < 4:
           return [self.pagination_link(i) for i in range(2,self.num_pages)]
        elif self.current_page < 4:
            return [self.pagination_link(i) for i in [2, 3, 4]] + empty_link
        elif self.current_page > self.num_pages -3:
            return empty_link +[self.pagination_link(i) for i in [self.num_pages -2, self.num_pages -1]]
        return  empty_link + [
                self.pagination_link(i) for i in [self.current_page -1, self.current_page, self.current_page +1]
            ] + empty_link
         
    def pagination_link(self, i):
            return {"n":i, "link": self.page(i)}
            

    def set_page_number_for_link(self, page_number):
        if "page=" in self.requesting_url:
            return re.sub(rf"(.*)page={self.current_page}(&|$)(.*)", rf"\1page={page_number}\2\3",self.requesting_url )
        return self.requesting_url + f"&page={page_number}" 

        


# dict_keys(['startIndex', 'itemsPerPage', 'index', 'totalResults', 
# 'responseTime', 'processingTime', 'items', 'title', 'description', 'query', 'urlParams'])
