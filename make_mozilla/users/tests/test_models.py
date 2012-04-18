from django.utils import unittest
from django.contrib.gis import geos

from make_mozilla.users import models

class UserProfileTest(unittest.TestCase):
    def test_latitude_can_be_set(self):
        user_profile = models.UserProfile()
        user_profile.latitude = 51.456

        self.assertEqual(user_profile.location, geos.Point(51.456, 0))
    
    def test_latitude_can_be_gotten(self):
        user_profile = models.UserProfile(location = geos.Point(42, 24))

        self.assertEqual(user_profile.latitude, 42.0)

    def test_longitude_can_be_gotten(self):
        user_profile = models.UserProfile(location = geos.Point(42, 24))

        self.assertEqual(user_profile.longitude, 24.0)

    def test_longitude_can_be_set(self):
        user_profile = models.UserProfile()
        user_profile.longitude = 51.456

        self.assertEqual(user_profile.location, geos.Point(0, 51.456))

