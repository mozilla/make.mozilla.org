import pytz
from datetime import datetime, timedelta

def event_name(event_json):
    return {'name': event_json['name']}

def event_times(event_json):
    tz = pytz.timezone(event_json['local_timezone'])
    db_datetime = datetime.strptime(
        event_json['start_datetime_system'],
        '%Y-%m-%d %H:%M:%S'
    )
    db_ammended_datetime = db_datetime.replace(tzinfo=pytz.utc)
    cleaned_date = db_ammended_datetime.astimezone(tz)
    start = cleaned_date.replace(tzinfo=pytz.utc)
    end = start + timedelta(minutes=int(event_json['duration']))
    return {'start': start, 'end': end}

def event_description(event_json):
    return {'description': event_json['description']}

def event_official(event_json):
    official = False
    if event_json['is_official'] == '1':
        official = True
    return {'official': official}

def venue_name(event_json):
    return {'name': event_json['venue_name']}

def venue_country(event_json):
    return {'country': event_json['venue_country']}

def venue_street_address(event_json):
    fields = ['venue_addr1', 'venue_addr2', 'venue_city', 'venue_state_cd', 'venue_zip']
    address_fields = [event_json[k] for k in fields if event_json[k]]
    return {'street_address': '\n'.join(address_fields)}

def venue_location(event_json):
    return {'latitude': float(event_json['latitude']), 'longitude': float(event_json['longitude'])}
