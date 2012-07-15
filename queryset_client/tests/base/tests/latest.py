from testcases import (
    TestServerTestCase,
    get_client
)
from django.core.management import call_command


class LatestTestCase(TestServerTestCase):

    def setUp(self):
        self.start_test_server()
        self.client = get_client()
        call_command('loaddata', 'small_data.json')

    def tearDown(self):
        self.stop_test_server()

    def test_latest1(self):
        latest = self.client.message.objects.latest("id")
        order = self.client.message.objects.order_by("-id")[0]
        self.assertTrue(latest.id == order.id)
