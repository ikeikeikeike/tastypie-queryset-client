from testcases import (
    TestServerTestCase,
    get_client
)
from django.core.management import call_command


class OrderByTestCase(TestServerTestCase):

    def setUp(self):
        self.start_test_server()
        self.client = get_client()
        call_command('loaddata', 'small_data.json')

    def tearDown(self):
        self.stop_test_server()

    def test_order1(self):
        for i in self.client.message.objects.order_by("-id")[0:30]:
            self.assertTrue(i)

        order1 =  self.client.message.objects.all().order_by("-id")[0:30]
        for i in order1:
            self.assertTrue(i)

        order2 =  self.client.message.objects.all().order_by("-id")
        for i, k in zip(order2.all(), order2):
            self.assertTrue(i.id == k.id)

        order3 =  self.client.message.objects.order_by("-id")
        for i, k in zip(order3.all(), order3):
            self.assertTrue(i.id == k.id)