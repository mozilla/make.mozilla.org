from django.contrib.gis import admin
from make_mozilla.events import models

admin.site.register(models.Event)
admin.site.register(models.EventKind)
admin.site.register(models.Venue, admin.GeoModelAdmin)

