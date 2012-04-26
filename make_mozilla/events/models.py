from django.contrib.gis.db import models
from django.contrib.gis import geos
from datetime import datetime

class Venue(models.Model):
    name = models.CharField(max_length=255)
    street_address = models.TextField() 
    country = models.CharField(max_length=255)
    location = models.PointField(blank=True)

    objects = models.GeoManager()

    def __init__(self, *args, **kwargs):
        super(Venue, self).__init__(*args, **kwargs)
        if self.location is None:
            self.location = geos.Point(0, 0)

    @property
    def latitude(self):
        return self.location.x
    
    @latitude.setter
    def latitude(self, value):
        self.location.x = value

    @property
    def longitude(self):
        return self.location.y

    @longitude.setter
    def longitude(self, value):
        self.location.y = value

def _upcoming(qs):
    return qs.filter(start__gte = datetime.now())

class Event(models.Model):
    name = models.CharField(max_length = 255)
    event_url = models.CharField(max_length = 255, blank = True)
    venue = models.ForeignKey(Venue)
    start = models.DateTimeField(null = True, blank = True)
    end = models.DateTimeField(null = True, blank = True)
    source_id = models.CharField(max_length = 255, blank = True)
    organiser_email = models.CharField(max_length = 255)

    objects = models.GeoManager()

    @classmethod
    def upcoming(self):
        return _upcoming(self.objects)

    @classmethod
    def near(self, latitude, longitude):
        point = geos.Point(float(longitude), float(latitude))
        return _upcoming(self.objects).filter(location__distance_lte=(point, geos.D(mi=20)))

