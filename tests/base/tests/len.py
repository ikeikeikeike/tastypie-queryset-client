from testcases import (
    TestServerTestCase,
    get_client
)
from .utils import FixtureMixin


class LenTestCase(FixtureMixin, TestServerTestCase):

    def setUp(self):
        self.start_test_server()
        self.client = get_client()
        super(LenTestCase, self).setUp()

    def tearDown(self):
        self.stop_test_server()

    def test_len1(self):
        message = self.client.message.objects.all()
        self.assertTrue(len(message) == self.client.message.objects.count())

    def test_len2(self):
        message = self.client.message.objects.all()
        self.assertTrue(len(message) == self.client.message.objects.all().count())