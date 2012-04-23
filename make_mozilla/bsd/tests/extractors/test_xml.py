from django.utils import unittest
from mock import patch, Mock
from nose.tools import eq_, ok_
from make_mozilla.bsd.tests.utils import xml_fixture

from make_mozilla.bsd.extractors import xml as extractors

def cf():
    return xml_fixture('constituent.xml')

class ExtractConstituentEmailTest(unittest.TestCase):
    def test_correct_email_is_retrieved(self):
        eq_(extractors.constituent_email(cf()), 'example@mozilla.org')
