from django.db import models

# Create your models here.

#TODO: add a model AccessSiteCollection that contains +1 AIT collection ids to serve as a map, + copy for collection pages, etc. 

class AccessSiteCollection(models.Model):
    display_name_en = models.CharField(max_length=500)
    display_name_fr = models.CharField(max_length=500)
    
    description_en = models.TextField()
    description_fr = models.TextField()

    feature_on_index_page = models.BooleanField(default=True)

    image = models.ImageField(default='canada.jpg')

    ait_collection_map = models.JSONField(default=list)
