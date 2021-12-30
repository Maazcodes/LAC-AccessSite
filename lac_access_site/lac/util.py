# LAC Access Site Utilities 
import requests

# get a csrf token to communicate with the partner site api
#def get_token():
    #TODO parametrize via settings
    #TODO set up a separate user with sane permissions
#    url = 'https://wbgrp-svc517:8080/login'
#    data = {"username":"pvisakan", "password":""}
#    headers = {"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
#               "Accept-Encoding":"gzip, deflate, br",
#               "Content-Type":"application/x-www-form-urlencoded",
#            }

#    token_response = requests.post(url, data)

#    print(token_response.text)

# hardcoded seed data for now
# seed urls AND LAC metadata can be found in AIT - to be pulled dynamically
# { collection_id : [ { seed: {data} } ...]
test_seed_store = {
    6602: [
        {"url":"http://www.thestar.com/opinion/commentary/2016/03/21/what-indigenous-reconciliation-means-for-millennials.html?utm_content=bufferb999e&utm_medium=social&utm_source=facebook.com&utm_campaign=buffer", "title":"What Indigenous reconciliation means for millennials", "topic":"Truth and Reconciliation Canada,Intergenerational relations,Intergenerational communication", "language":"EN"},
        {"url":"http://www.theglobeandmail.com/globe-debate/building-a-bright-future-for-first-nations-and-the-our-new-government/article27641116/", "title":"How to build a bright future for First Nations and our new government", "topic":"Indigenous peoples--Canada—Government relations", "language":"EN"},
        {"url":"http://www.ledevoir.com/politique/canada/470481/terre-neuve-et-labrador-entente-de-50-millions-pour-les-pensionnats-autochtones", "title":"Entente de 50 millions pour les pensionnats autochtones", "topic":"Residential school survivors,Indigenous peoples--Canada—Government relations", "language":"FR"}
    ],

    9155:[
        {"url":"http://www.collectionscanada.gc.ca/archivianet/02011703_e.html", "title":"[Philatis image database]", "department": None},
        {"url":"http://www.collectionscanada.gc.ca/archivianet/02011702_f.html", "title":None, "department": None},
        {"url":"http://data4.collectionscanada.gc.ca/netacgi/nph-brs?s1=(?.ANYP.)%20Or%20(?.ANYI.%20And%20null.B742.)&l=0&d=STMP&p=1&u=http://www.collectionscanada.gc.ca/archivianet/02011702_e.html&r=0&f=S&Sect1=STMP", "title":"[Philatis] Canadian Postal Archives Database", "department": None},
    ],

    13693:[]
}

# use http to fetch results from the partner site's api
def get_seeds(collection_id, token):
    # TODO pull dynamically from ait http api
    return test_seed_store[collection_id]
