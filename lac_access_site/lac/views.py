from django.shortcuts import render
from lac.util import get_seeds
#from django.http import HttpResponse

# Create your views here.

def index(request):
    return render(request, 'lac/index.html', {})

def search(request):
    return render(request, 'lac/search.html', {})

def collection(request, lac_collection_id):
    #TODO render using db collections
    #TODO distinguish between LAC and goc collections
    collection_type = "lac" if lac_collection_id != 9155 else "goc"
    context = {"seed_data": get_seeds(lac_collection_id, None), "id":lac_collection_id, "type":collection_type}

    print(context)
    return render(request, 'lac/collection.html', context)

