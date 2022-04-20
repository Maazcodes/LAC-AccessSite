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
    query = request.GET.get("q","")
    access_site_collection_id = request.GET.get("i","all")

    if access_site_collection_id == 'all':
        collections = [collection.ait_collection_map for collection in AccessSiteCollection.objects.filter(feature_on_index_page=True)]
    else:
        collections = AccessSiteCollection.objects.get(pk=access_site_collection_id).ait_collection_map

    results = get_search_results(query, collections, request)
    return render(request, 'lac/search.html', {'results':results, "collection" : collection})

def search_page(request):
    query = request.GET.get("q","")
    selected_collection = request.GET.get("i","all")
    if selected_collection.isnumeric():
        selected_collection = int(selected_collection)

    collections = AccessSiteCollection.objects.all()
    return render(request, 'lac/search-page.html', {"collections":collections, "query" :query, "selected_collection": selected_collection })

def advanced_search_page(request):
    collections = AccessSiteCollection.objects.all()
    return render(
        request, 
        'lac/advanced-search-page.html', 
        {
            "collections":collections
        }
    )

def collection(request, lac_collection_id):
    collection = AccessSiteCollection.objects.get(pk=lac_collection_id)

    seed_data = get_seeds(collection.ait_collection_map)

    context = {"seed_data": seed_data["data"], "topics": seed_data["topics"], "collection":collection}

    #print(context)
    return render(request, 'lac/collection.html', context)

def test(request):
    collections = AccessSiteCollection.objects.all()
    return render(request, 'lac/test.html', {"collections":collections})
