import cronjobs
from django.conf import settings
from make_mozilla.news.tasks import parse_feed
from make_mozilla.news.models import Article
import commonware.log
import funfactory.log_settings  # Magic voodoo required to make logging work.

log = commonware.log.getLogger('mk.cron')


@cronjobs.register
def update_site_feeds():
    ids = []
    feeds = getattr(settings, 'SITE_FEED_URLS', None)
    for page, feed_url in feeds.iteritems():
        log.info('Importing articles for %s from $s') % (page, feed_url)
        parsed = parse_feed(feed_url, page)
        ids.extend(parsed)
    Article.objects.exclude(id__in=ids).delete()
