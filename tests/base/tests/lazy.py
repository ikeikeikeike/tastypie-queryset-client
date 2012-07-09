from testcases import (
    TestServerTestCase,
    get_client
)


class LazyTestCase(TestServerTestCase):

    def setUp(self):
        self.start_test_server()
        self.client = get_client()

    def tearDown(self):
        self.stop_test_server()

    # TODO: input prepend data
    def test_lazy1(self):
        fl = self.client.inbox_message_many.objects.filter()
        if 0 < len(fl):
            self.assertTrue(fl)
            for f in fl:
                self.assertTrue(f)