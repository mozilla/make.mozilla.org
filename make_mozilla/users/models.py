from django.contrib.gis.db import models
from django.contrib.gis import geos

from django.contrib.auth.models import User

class UserProfile(models.Model):
    user     = models.OneToOneField(User, primary_key=True)
    country  = models.CharField(max_length=255, blank=True)
    city     = models.CharField(max_length=255, blank = True)
    location = models.PointField(blank=True)

    def _location(self):
        if self.location is None:
            self.location = geos.Point(0, 0)
        return self.location

    @property
    def latitude(self):
        return self._location().x
    
    @latitude.setter
    def latitude(self, value):
        self._location().x = value

    @property
    def longitude(self):
        return self._location().y

    @longitude.setter
    def longitude(self, value):
        self._location().y = value
