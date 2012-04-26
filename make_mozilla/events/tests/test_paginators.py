from django.utils import unittest
from nose.tools import eq_, ok_

from make_mozilla.events.paginators import results_page

sample_results = [1,2,3,4,5,6,7,8,9,0]

class TestResultsPage(unittest.TestCase):
    def test_returns_page_1_if_page_unspecified(self):
        page = results_page(sample_results, 4)
        
        eq_(page.number, 1)

    def test_returns_page_2_if_asked_for_it(self):
        page = results_page(sample_results, 4, page = '2')

        eq_(page.number, 2)

    def test_returns_page_1_if_asked_for_a_non_number(self):
        page = results_page(sample_results, 4, page = 'NaN')
        
        eq_(page.number, 1)

    def test_returns_page_3_if_asked_for_a_page_gt_3(self):
        page = results_page(sample_results, 4, page = '4')

        eq_(page.number, 3)

    def test_still_returns_something_if_there_are_no_results(self):
        page = results_page([], 4)
        
        eq_(page.number, 1)
