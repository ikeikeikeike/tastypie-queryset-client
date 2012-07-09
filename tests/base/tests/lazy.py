from testcases import (
    TestServerTestCase,
    get_client
)
from .utils import FixtureMixin


class LazyTestCase(FixtureMixin, TestServerTestCase):

    def setUp(self):
        self.start_test_server()
        self.client = get_client()
        super(LazyTestCase, self).setUp()

    def tearDown(self):
        self.stop_test_server()

    def test_lazy1(self):
        fl = self.client.inbox_message_many.objects.filter()
        self.assertTrue(fl)
        for f in fl:
            self.assertTrue(f)