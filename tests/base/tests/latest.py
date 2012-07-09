from testcases import (
    TestServerTestCase,
    get_client
)
from .utils import FixtureMixin


class LatestTestCase(FixtureMixin, TestServerTestCase):

    def setUp(self):
        self.start_test_server()
        self.client = get_client()
        super(LatestTestCase, self).setUp()

    def tearDown(self):
        self.stop_test_server()

    def test_latest1(self):
        latest = self.client.message.objects.latest("id")
        order = self.client.message.objects.order_by("-id")[0]
        self.assertTrue(latest.id == order.id)
