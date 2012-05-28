import time
import urllib2
import feedparser
import hashlib
import bleach

from django.conf import settings
from django.utils.encoding import smart_str

from make_mozilla.news.models import Article


def parse_entry(entry):
    title = getattr(entry, 'title', None)
    link = getattr(entry, 'link', None)
    author = getattr(entry, 'author', None)
    updated = getattr(entry, 'updated_parsed', None)
    summary = getattr(entry, 'summary', None)
    cleaned_title = title.split(':')
    if author == None:
        author = cleaned_title[0]
    return {
        'title': cleaned_title[1],
        'link': link,
        'author': author,
        'updated_on': updated,
        'summary': summary,
    }


def get_feed_entries(feed_url):
    data = urllib2.urlopen(feed_url).read()
    feed = feedparser.parse(data)
    entries = feed.entries
    return entries


def parse_feed(feed_url, page):
    ids = []
    entries = get_feed_entries(feed_url)
    for entry in entries:
        parsed = parse_entry(entry)
        clean_summary = smart_str(bleach.clean(parsed['summary'],
            tags=settings.BLEACH.allowed_tags,
            attributes=settings.BLEACH.allowed_attrs,
            strip=True))
        checksum = hashlib.md5(clean_summary + page).hexdigest()
        exists = Article.objects.filter(checksum=checksum)
        if not exists:
            entry = Article(
                title=parsed['title'].encode('utf-8'),
                link=parsed['link'].encode('utf-8'),
                summary=clean_summary,
                page=page,
                checksum=checksum,
                updated=time.strftime(
                    "%Y-%m-%d", parsed['updated_on']),
                autor=parsed['author'])
            entry.save()
            entry_id = entry.id
        else:
            entry_id = exists[0].id
        ids.append(entry_id)
    return ids


def update_site_feeds():
    ids = []
    feeds = getattr(settings, 'SITE_FEED_URLS', None)
    for page, feed_url in feeds.iteritems():
        parsed = parse_feed(feed_url, page)
        ids.extend(parsed)
    Article.objects.exclude(id__in=ids).delete()
