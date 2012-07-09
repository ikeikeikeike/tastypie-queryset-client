#from django.conf import settings
#settings.DEBUG = True
from testcases import (
    TestServerTestCase,
    get_client
)
from .utils import FixtureMixin


class CountTestCase(FixtureMixin, TestServerTestCase):

    def setUp(self):
        self.start_test_server()
        self.client = get_client()
        super(CountTestCase, self).setUp()

    def tearDown(self):
        self.stop_test_server()

    def test_count1(self):
        num = self.client.message.objects.count()
        self.assertTrue(-1 < num)
        self.assertTrue(isinstance(num, int))

    def test_count2(self):
        nums = self.client.message.objects.filter(id__in=xrange(0, 12))
        num = nums.count()
        assert 11 == num
        assert isinstance(num, int)