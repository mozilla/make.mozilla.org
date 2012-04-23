import os.path
import json

def fixture_path(path):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), path))

def json_fixture(fixture_name):
    return json.load(open(fixture_path('fixtures/%s' % fixture_name)))

def xml_fixture(fixture_name):
    return open(fixture_path('fixtures/%s' % fixture_name)).read()
