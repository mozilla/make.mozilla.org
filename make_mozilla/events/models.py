from django.contrib.gis.db import models
from django.contrib.gis import geos, measure
from django_countries import CountryField
from django.utils.safestring import mark_safe
from datetime import datetime

class Venue(models.Model):
    name = models.CharField(max_length=255)
    street_address = models.TextField()
    country = CountryField()
    location = models.PointField(blank=True)

    objects = models.GeoManager()

    def __init__(self, *args, **kwargs):
        super(Venue, self).__init__(*args, **kwargs)
        if self.location is None:
            longitude = float(kwargs.get('longitude', '0'))
            latitude = float(kwargs.get('latitude', '0'))
            self.location = geos.Point(longitude, latitude)

    @property
    def latitude(self):
        return self.location.y
    
    @latitude.setter
    def latitude(self, value):
        self.location.y = value

    @property
    def longitude(self):
        return self.location.x

    @longitude.setter
    def longitude(self, value):
        self.location.x = value

def _upcoming(qs):
    return qs.filter(start__gte = datetime.now())

class Event(models.Model):
    name = models.CharField(max_length = 255)
    description = models.TextField()
    event_url = models.URLField(blank = True)
    venue = models.ForeignKey(Venue)
    start = models.DateTimeField(null = True, blank = True)
    end = models.DateTimeField(null = True, blank = True)
    source_id = models.CharField(max_length = 255, blank = True)
    organiser_email = models.EmailField(max_length = 255)
    campaign = models.ForeignKey('Campaign', null = True)
    kind = models.ForeignKey('EventKind', null = True)
    verified = models.BooleanField(default = False)
    official = models.BooleanField(default = False)
    public = models.BooleanField(default = False)

    objects = models.GeoManager()

    @classmethod
    def upcoming(self):
        return _upcoming(self.objects)

    @classmethod
    def near(self, latitude, longitude):
        point = geos.Point(float(longitude), float(latitude))
        return _upcoming(self.objects).filter(venue__location__distance_lte=(point, measure.D(mi=20)))

class Campaign(models.Model):
    name = models.CharField(max_length = 255)
    description = models.TextField()
    slug = models.SlugField()
    start = models.DateField()
    end = models.DateField()

class EventKind(models.Model):
    name = models.CharField(max_length = 255)
    description = models.TextField()
    slug = models.SlugField()

    def __unicode__(self):
        return mark_safe(u'<strong>%s</strong> <span>%s</span>' % (self.name, self.description))
