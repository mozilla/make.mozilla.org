import json, urllib2

import bsdapi

def parse_event_feed(feed_url):
    return process_events_json(json.load(urllib2.urlopen(feed_url)))

def process_events_json(events_json):
    return [event['id'] for event in events_json['results']]

