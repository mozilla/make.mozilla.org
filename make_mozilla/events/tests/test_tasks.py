from django.utils import unittest
from mock import patch, Mock
from nose.tools import eq_, ok_

from make_mozilla.events import tasks

class AddOrganiserAsConstituentTaskTest(unittest.TestCase):
    @patch.object(tasks.BSDClient, 'register_email_address_as_constituent')
    def test_task_func_correctly_invokes_bsd_client(self, mock_client_func):
        mock_client_func.return_value = True

        tasks.register_email_address_as_constituent('example@mozilla.org')

        mock_client_func.assert_called_with('example@mozilla.org')
