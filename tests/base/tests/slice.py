from testcases import (
    TestServerTestCase,
    get_client
)


class SliceTestCase(TestServerTestCase):

    def setUp(self):
        self.start_test_server()
        self.client = get_client()

    def tearDown(self):
        self.stop_test_server()
    
    def test_slice1(self):
        al = self.client.inbox.objects.all()
        for i in al[0:8]:
            self.assertTrue(i)
    
    def test_slice2(self):
        al = self.client.inbox_message_many.objects.all()
        for i in al[0:10]:
            self.assertTrue(i)
