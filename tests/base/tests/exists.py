#from django.conf import settings
#settings.DEBUG = True
from django.core.management import call_command
from testcases import (
    TestServerTestCase,
    get_client
)


class ExistsTestCase(TestServerTestCase):

    def setUp(self):
        self.start_test_server()
        self.client = get_client()
        call_command('loaddata', 'small_data.json')

    def tearDown(self):
        self.stop_test_server()

    def test_exists1(self):
        message = self.client.message.objects.exists()
        self.assertTrue(message is True)
        message = self.client.message.objects.all().exists()
        self.assertTrue(message is True)
        message = self.client.message.objects.filter(id=10000000)
        exists = message.exists()
        self.assertTrue(exists is False)