from testcases import (
    TestServerTestCase,
    get_client
)


class OrderByTestCase(TestServerTestCase):

    def setUp(self):
        self.start_test_server()
        self.client = get_client()

    def tearDown(self):
        self.stop_test_server()

    def test_order1(self):
        for i in self.client.message.objects.order_by("-id")[0:30]:
            self.assertTrue(i)

    def test_order2(self):
        order =  self.client.message.objects.all().order_by("-id")[0:30]
        for i in order:
            self.assertTrue(i)

    def test_order3(self):
        order =  self.client.message.objects.all().order_by("-id")
        for i, k in zip(order.all(), order):
            self.assertTrue(i.id == k.id)

    def test_order4(self):
        order =  self.client.message.objects.order_by("-id")
        for i, k in zip(order.all(), order):
            self.assertTrue(i.id == k.id)