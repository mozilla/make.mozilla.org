import cronjobs
from django.conf import settings
from make_mozilla.bsd import fetch_and_process_event_feed
from make_mozilla.events import models
import commonware.log
import funfactory.log_settings # Magic voodoo required to make logging work.

log = commonware.log.getLogger('mk.cron')

@cronjobs.register
def import_bsd_events():
    log.info('Running import_bsd_events')
    for kind_slug, url in settings.BSD_EVENT_JSON_FEED_URLS:
        import_bsd_events_for_kind_and_url(kind_slug, url)

def import_bsd_events_for_kind_and_url(kind_slug, url):
    event_kind = models.EventKind.objects.get(slug = kind_slug)
    fetch_and_process_event_feed(event_kind, url)

