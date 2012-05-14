from django.conf import settings
from django.contrib.gis.db import models
from django.contrib.gis import geos, measure
from django_countries import CountryField
from django.utils.safestring import mark_safe
from django.core.files.storage import FileSystemStorage

from datetime import datetime
from tower import ugettext_lazy as _

from make_mozilla.base.html import bleached

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

    def __unicode__(self):
        return '%s - %s, %s' % (self.name, self.street_address,  self.country)

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

def _upcoming(qs, sort, include_private):
    resultset = qs.filter(start__gte = datetime.now(), verified = True).order_by(sort)
    if not include_private:
        resultset = resultset.filter(public=True)
    return resultset

class Event(models.Model):
    name = models.CharField(max_length = 255)
    description = models.TextField()
    event_url = models.URLField(blank = True)
    venue = models.ForeignKey(Venue)
    start = models.DateTimeField(null = True, blank = True)
    end = models.DateTimeField(null = True, blank = True)
    source_id = models.CharField(max_length = 255, blank = True)
    organiser_email = models.EmailField(max_length = 255)
    campaign = models.ForeignKey('Campaign', null = True, blank=True)
    kind = models.ForeignKey('EventKind', null = True)
    verified = models.BooleanField(default = False)
    official = models.BooleanField(default = False)
    public = models.BooleanField(default = False)

    objects = models.GeoManager()

    def __unicode__(self):
        return self.name

    @property
    def bleached_description(self):
        return bleached(self.description)

    @classmethod
    def upcoming(self, sort='start', include_private=False):
        return _upcoming(self.objects, sort, include_private)

    @classmethod
    def near(self, latitude, longitude, sort='start', include_private=False):
        point = geos.Point(float(longitude), float(latitude))
        return _upcoming(self.objects, sort, include_private).filter(venue__location__distance_lte=(point, measure.D(mi=20)))

class Campaign(models.Model):
    name = models.CharField(max_length = 255)
    description = models.TextField()
    logo = models.ImageField(upload_to = 'campaigns', storage = FileSystemStorage(**settings.UPLOADED_IMAGES))
    slug = models.SlugField()
    start = models.DateField()
    end = models.DateField()

    def __unicode__(self):
        return '%s - %s to %s' % (self.name, self.start, self.end)

class EventKind(models.Model):
    name = models.CharField(max_length = 255)
    description = models.TextField()
    additional = models.TextField(blank=True, null=True)
    slug = models.SlugField()

    def __unicode__(self):
        return mark_safe(u'%s' % (self.name))


class Partner(models.Model):
    name = models.CharField(max_length=255)
    website = models.URLField()
    logo = models.ImageField(upload_to = 'partners', storage = FileSystemStorage(**settings.UPLOADED_IMAGES))
    featured = models.BooleanField(default=False,
        help_text=_(u'Featured partners are displayed on the home and campaign page'))
    for_campaign = models.ForeignKey(Campaign)

    def __unicode__(self):
        return self.name

