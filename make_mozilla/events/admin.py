from django.contrib.gis import admin

from make_mozilla.events import models


class EventAdmin(admin.ModelAdmin):
    model = models.Event
    list_display = ('name', 'kind', 'venue', 'source_id')
    list_filter = ('kind', 'campaign', 'verified', 'official', 'public')
    exclude = ('url_hash',)
    date_hierarchy = 'start'


class PartnerAdmin(admin.ModelAdmin):
    model = models.Partner
    list_display = ('name', 'featured',)
    list_filter = ('featured',)


admin.site.register(models.Event, EventAdmin)
admin.site.register(models.EventKind)
admin.site.register(models.Venue, admin.GeoModelAdmin)
admin.site.register(models.Campaign)
admin.site.register(models.Partner, PartnerAdmin)
