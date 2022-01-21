from django.shortcuts import render
from lac.util import get_seeds, get_search_results
#from django.http import HttpResponse

# Create your views here.
# TODO add some malformed request handling - 404 etc

def index(request):
    return render(request, 'lac/index.html', {})

def search(request):
    query = request.GET["q"]
    collections = request.GET["i"]

    results = get_search_results(query, collections, request.GET)
    
    return render(request, 'lac/search.html', {'results':results})

def search_page(request):
    return render(request, 'lac/search-page.html', {})

def advanced_search_page(request):
    return render(request, 'lac/advanced-search-page.html', {})

def collection(request, lac_collection_id):
    #TODO render using db collections
    #TODO distinguish between LAC and goc collections
    collection_type = "lac" if lac_collection_id != 9155 else "goc"
    context = {"seed_data": get_seeds(lac_collection_id), "id":lac_collection_id, "type":collection_type}

    #print(context)
    return render(request, 'lac/collection.html', context)

