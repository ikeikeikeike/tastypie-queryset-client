#from django.conf import settings
#settings.DEBUG = True
from testcases import (
    TestServerTestCase,
    get_client
)


class ForeignkeyTestCase(TestServerTestCase):

    def setUp(self):
        self.start_test_server()
        self.client = get_client()

    def tearDown(self):
        self.stop_test_server()

    # TODO: input prepend data
    def test_foreignkey1(self):

        if 0 < self.client.inbox_message.objects.count():
            self.assertTrue(self.client.inbox_message.objects.all()[0].message.id)
            self.assertTrue(self.client.inbox_message.objects.all()[1].message.id)
            self.assertTrue(self.client.inbox_message.objects.all()[2].message.id)

        try:
            self.client.inbox_message.objects.all()[99999]
        except IndexError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)
