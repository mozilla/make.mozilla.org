import json, urllib2

import bsdapi

def parse_event_feed(feed_url):
    return process_events_json(json.load(urllib2.urlopen(feed_url)))

def process_events_json(events_json):
    return [event['id'] for event in events_json['results']]

class BSDEventImporter(object):
    event_extractors = []
    venue_extractors = []

    @classmethod
    def extract_from_event_json(self, event_json):
        pass

    def __init__(self, event_feed_url):
        self.event_feed_url = event_feed_url
