#from django.conf import settings
#settings.DEBUG = True
from testcases import (
    TestServerTestCase,
    get_client
)
from queryset_client.client import (
    MultipleObjectsReturned,
    ObjectDoesNotExist
)
from .utils import id_generator



class GetOrCreateTestCase(TestServerTestCase):

    def setUp(self):
        self.start_test_server()
        self.client = get_client()

    def tearDown(self):
        self.stop_test_server()

    def test_get_or_create1(self):
        subject = "subject get_or_create 1 - {0}".format(id_generator())
        body = "body get_or_create 1 - {0}".format(id_generator())

        message, created = self.client.message.objects.get_or_create(subject=subject, body=body)

        message_ = self.client.message.objects.get(id=message.id, subject=subject, body=body)
        self.assertTrue(message_.id == message.id)
        self.assertTrue(message_.subject == message.subject)
        self.assertTrue(message_.body == message.body)


    def test_get_or_create2(self):
        subject1 = "subject get_or_create 2 - {0}".format(id_generator())
        body1 = "body get_or_create 2 - {0}".format(id_generator())

        message, created = self.client.message.objects.get_or_create(subject=subject1, body=body1)

        subject2 = "subject get_or_create 2 update"
        body2 = "body get_or_create 2 update"
        message.subject = subject2
        message.body = body2
        message.save()
        try:
            self.client.message.objects.get(id=message.id, subject=subject1, body=body1)
        except ObjectDoesNotExist:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

        try:
            message_ = self.client.message.objects.get(id=message.id, subject=subject2, body=body2)
        except ObjectDoesNotExist:
            self.assertTrue(False)
        else:
            self.assertTrue(True)
            self.assertTrue(message_.id == message.id)
            self.assertTrue(message_.subject == message.subject)
            self.assertTrue(message_.body == message.body)


    def test_get_or_create3(self):
        subject1 = "subject get_or_create 3 - {0}".format(id_generator())
        body1 = "body get_or_create 3 - {0}".format(id_generator())

        message = self.client.message(subject=subject1, body=body1)
        message.save()

        message_, created = self.client.message.objects.get_or_create(subject=subject1, body=body1)
        self.assertTrue(message_.id == message.id)
        self.assertTrue(message_.subject == message.subject == subject1)
        self.assertTrue(message_.body == message.body == body1)


    def test_get_or_create4(self):
        subject1 = "subject get_or_create 4"
        body1 = "body get_or_create 4"

        message = self.client.message(subject=subject1, body=body1)
        message.save()

        message = self.client.message(subject=subject1, body=body1)
        message.save()

        try:
            self.client.message.objects.get_or_create(subject=subject1, body=body1)
        except MultipleObjectsReturned:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

