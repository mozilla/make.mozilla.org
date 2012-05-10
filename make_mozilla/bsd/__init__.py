import json, urllib2, re

from bsdapi.BsdApi import Factory as BSDApiFactory
from django.conf import settings
from make_mozilla.events.models import Event, Venue
from make_mozilla.bsd.extractors import json as json_extractors
from make_mozilla.bsd.extractors import xml as xml_extractors
import email.parser
import commonware.log
import funfactory.log_settings # Magic voodoo required to make logging work.

log = commonware.log.getLogger('mk.bsd')

def parse_event_feed(feed_url):
    return process_events_json(json.load(urllib2.urlopen(feed_url)))

def process_events_json(events_json):
    return [event['url'] for event in events_json['results']]

def fetch_and_process_event_feed(event_kind, feed_url):
    [BSDEventImporter.process_event(event_kind, url) for url in parse_event_feed(feed_url)]

class BSDClient(object):
    @classmethod
    def _request(cls, http_method, endpoint, api_params):
        client = cls.create_api_client()
        response = client.doRequest(endpoint,
                api_params = api_params,
                request_type = http_method,
                https = True)
        return response

    @classmethod
    def _get(cls, endpoint, api_params):
        return cls._request('GET', endpoint, api_params)

    @classmethod
    def _post(cls, endpoint, api_params):
        return cls._request('POST', endpoint, api_params)

    @classmethod
    def fetch_event(cls, obfuscated_event_id):
        response = cls._get('/event/get_event_details',
                {'values': json.dumps({'event_id_obfuscated': obfuscated_event_id})})
        return json.loads(response.body)

    @classmethod
    def _api_response_charset(cls, api_response):
        content_type_header = api_response.http_response.getheader('content-type',
                'text/xml; charset=utf-8')
        m = email.parser.Parser().parsestr("Content-Type: %s" % content_type_header)
        charset = (m.get_param('charset') or 'utf-8')
        return charset

    @classmethod
    def constituent_email_for_constituent_id(cls, constituent_id):
        response = cls._get('/cons/get_constituents_by_id',
                {'cons_ids': constituent_id, 'bundles': 'primary_cons_email'})
        charset = cls._api_response_charset(response)
        return xml_extractors.constituent_email(response.body.encode(charset))

    @classmethod
    def create_api_client(cls):
        client_params = {'port': 80, 'securePort': 443}
        client_params.update(settings.BSD_API_DETAILS)
        return BSDApiFactory().create(**client_params)

    @classmethod
    def register_email_address_as_constituent(cls, email_address):
        response = cls._post('/cons/email_register',
                {'email': email_address, 'format': 'json'})
        if response.http_status == 200:
            api_response = json.loads(response.body)
            return api_response[0]['cons_id']
        raise BSDApiError("%s: %s" % (response.http_status, response.http_reason))

    @classmethod
    def add_constituent_id_to_group(cls, cons_id, group_id):
        response = cls._post('/cons_group/add_cons_ids_to_group',
                {'cons_ids': cons_id, 'cons_group_id': group_id})
        return response.http_status == 202

class BSDRegisterConstituent(object):
    @classmethod
    def add_email_to_group(cls, email, group_id):
        constituent_id = BSDClient.register_email_address_as_constituent(email)
        result = BSDClient.add_constituent_id_to_group(constituent_id, group_id)
        if not result:
            log.warning('Failed to add email to group')
        return result

class BSDEventImporter(object):
    @classmethod
    def extract_event_obfuscated_id(cls, event_url):
        return re.split(r'/', event_url)[-1]

    @classmethod
    def process_event(cls, event_kind, event_url):
        obfuscated_id = cls.extract_event_obfuscated_id(event_url)
        event_json = BSDClient.fetch_event(obfuscated_id)
        # BSDEventImporter() rather than cls() because of test mocking
        BSDEventImporter().process_event_from_json(event_kind, event_url, event_json)

    def event_extractors(self):
        return [json_extractors.event_name, json_extractors.event_times, json_extractors.event_description]

    def venue_extractors(self):
        return [json_extractors.venue_name, json_extractors.venue_country, 
                json_extractors.venue_street_address, json_extractors.venue_location]

    def event_source_id(self, event_json):
        return 'bsd:%s' % event_json['event_id']

    def fetch_existing_event(self, source_id):
        try:
            return Event.objects.get(source_id = source_id)
        except Event.DoesNotExist:
            return None

    def fetch_organiser_email_from_bsd(self, event_json):
        constituent_id = event_json['creator_cons_id']

        return BSDClient.constituent_email_for_constituent_id(constituent_id)

    def venue_for_event(self, event):
        if event.id is not None:
            return event.venue
        return Venue()

    def are_model_instances_identical(self, instance1, instance2):
        if not (type(instance1) == type(instance2)):
            return False
        local_fields = [f for f in instance1._meta.local_fields if not f.primary_key]
        def comparator(initial, field):
            return initial and (field.value_from_object(instance1) == field.value_from_object(instance2))
        return reduce(comparator, local_fields, True)

    def extract_from_event_json(self, event_json):
        event_attrs = {}
        [event_attrs.update(f(event_json)) for f in self.event_extractors()]
        venue_attrs = {}
        [venue_attrs.update(f(event_json)) for f in self.venue_extractors()]
        return {'event': event_attrs, 'venue': venue_attrs}

    def new_models_from_json(self, event_json):
        model_data = self.extract_from_event_json(event_json)
        event = Event(**model_data['event'])
        venue = Venue(**model_data['venue'])
        return (event, venue)

    def process_event_from_json(self, event_kind, event_url, event_json):
        source_id = self.event_source_id(event_json)
        event = self.fetch_existing_event(source_id)
        if event is None:
            event = Event()
        organiser_email = self.fetch_organiser_email_from_bsd(event_json)
        venue = self.venue_for_event(event)
        (new_event, new_venue) = self.new_models_from_json(event_json)
        new_event.event_url = event_url
        new_event.source_id = source_id
        new_event.organiser_email = organiser_email
        if not self.are_model_instances_identical(venue, new_venue):
            venue = new_venue
        venue.save()
        if not self.are_model_instances_identical(event, new_event):
            if event.id:
                new_event.id = event.id
            event = new_event
        if event.id:
            log.info('Updating event %s from %s' % (event.id, event_url))
        else:
            log.info('Adding new event for %s' % event_url)
        event.kind = event_kind
        event.venue = venue
        event.public = True
        event.verified = True
        event.save()

class BSDApiError(BaseException):
    pass
