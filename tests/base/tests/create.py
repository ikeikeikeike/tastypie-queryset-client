#from django.conf import settings
#settings.DEBUG = True
from testcases import (
    TestServerTestCase,
    get_client
)

class CreateTestCase(TestServerTestCase):
    def setUp(self):
        self.start_test_server()
        self.client = get_client()

    def tearDown(self):
        self.stop_test_server()

    def test_create1(self):
        subject = "subject create 1"
        body = "body create 1"
        message = self.client.message.objects.create(subject=subject, body=body)

        message_ = self.client.message.objects.get(id=message.id, subject=subject, body=body)
        self.assertTrue(message_.id == message.id)
        self.assertTrue(message_.subject == message.subject)
        self.assertTrue(message_.body == message.body)
