from make_mozilla.events.models import Event, Venue, Campaign, EventKind
from django.contrib import admin

admin.site.register(Event)
admin.site.register(Venue)
admin.site.register(Campaign)
admin.site.register(EventKind)
