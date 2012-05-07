from django.contrib.gis import admin
from make_mozilla.events import models


class EventAdmin(admin.ModelAdmin):
    model = models.Event
    list_display = ('name', 'kind', 'venue')
    list_filter = ('kind', 'campaign', 'verified', 'official', 'public')


admin.site.register(models.Event, EventAdmin)
admin.site.register(models.EventKind)
admin.site.register(models.Venue, admin.GeoModelAdmin)
admin.site.register(models.Campaign)

