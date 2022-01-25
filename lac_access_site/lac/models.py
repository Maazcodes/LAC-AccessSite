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

    LAC = 'lac'
    GOC = 'goc'

    COLLECTION_TYPE_CHOICES = [(LAC, 'Library Archives Canada'),(GOC, 'Government of Canada')]

    collection_type = models.CharField(choices=COLLECTION_TYPE_CHOICES, max_length=3, default=LAC)

    ait_collection_map = models.JSONField(default=list)

    def __str__(self):
        return self.display_name_fr + " | " + self.display_name_en 
