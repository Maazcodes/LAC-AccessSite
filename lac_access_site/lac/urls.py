from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('collection/<int:lac_collection_id>/', views.collection, name='collection'),
    path('search', views.search, name='search'),
    path('search-results', views.search_page, name='search-results'),
    #TODO consolidate into one search results page with a dropdown
    path('advanced-search-results', views.advanced_search_page, name='advanced-search-results'),
]
