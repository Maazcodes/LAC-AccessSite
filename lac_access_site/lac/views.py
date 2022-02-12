from django.shortcuts import render
from lac.models import AccessSiteCollection
from lac.util import get_seeds, get_search_results
#from django.http import HttpResponse

# Create your views here.
# TODO add some malformed request handling - 404 etc

def index(request):
    collections = AccessSiteCollection.objects.all()
    return render(request, 'lac/index.html', {"collections":collections})

def search(request):
    query = request.GET["q"]
    access_site_collection_id = request.GET["i"]

    if access_site_collection_id == 'all':
        collections = [collection.ait_collection_map for collection in AccessSiteCollection.objects.all()]
    else:
        collections = AccessSiteCollection.objects.get(pk=access_site_collection_id).ait_collection_map

    results = get_search_results(query, collections, request.GET)
    
    return render(request, 'lac/search.html', {'results':results})

def search_page(request):
    collections = AccessSiteCollection.objects.all()
    return render(request, 'lac/search-page.html', {"collections":collections})

def advanced_search_page(request):
    collections = AccessSiteCollection.objects.all()
    return render(request, 'lac/advanced-search-page.html', {"collections":collections})

def collection(request, lac_collection_id):
    collection = AccessSiteCollection.objects.get(pk=lac_collection_id)

    seed_data = get_seeds(collection.ait_collection_map)

    context = {"seed_data": seed_data["data"], "topics": seed_data["topics"], "collection":collection}

    #print(context)
    return render(request, 'lac/collection.html', context)

def test(request):
    collections = AccessSiteCollection.objects.all()
    return render(request, 'lac/test.html', {"collections":collections})
