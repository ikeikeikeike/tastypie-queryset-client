#from django.conf import settings
#settings.DEBUG = True
from testcases import (
    TestServerTestCase,
    get_client
)
from .utils import FixtureMixin


class ExistsTestCase(FixtureMixin, TestServerTestCase):

    def setUp(self):
        self.start_test_server()
        self.client = get_client()
        super(ExistsTestCase, self).setUp()

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