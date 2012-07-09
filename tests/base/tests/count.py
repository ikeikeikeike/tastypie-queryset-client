#from django.conf import settings
#settings.DEBUG = True
from testcases import (
    TestServerTestCase,
    get_client
)

class CountTestCase(TestServerTestCase):
    def setUp(self):
        self.start_test_server()
        self.client = get_client()

    def tearDown(self):
        self.stop_test_server()

    def test_count1(self):
        num = self.client.inbox_message_many.objects.count()
        self.assertTrue(-1 < num)
        self.assertTrue(isinstance(num, int))

#    def test_count2(self):
#        # TODO: fixture
#        nums = self.client.inbox_message_many.objects.filter(id__in=xrange(0, 12))
#        num = nums.count()
#        assert 11 == num
#        assert isinstance(num, int)