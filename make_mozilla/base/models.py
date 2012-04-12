from django.contrib.gis.db import models

class Event(models.Model):
    name = models.CharField(max_length=255)
    venue_name = models.CharField(max_length=255, blank=True)
    venue_address = models.TextField()
    country = models.CharField(max_length=255)
    event_url = models.CharField(max_length=255)
    location = models.PointField(blank=True)

    objects = models.GeoManager()
