from datetime import datetime
#from django.conf import settings
#settings.DEBUG = True
from testcases import (
    TestServerTestCase,
    get_client
)
from django.core.management import call_command
from .utils import id_generator


class StrictTestCase(TestServerTestCase):

    def setUp(self):
        self.start_test_server()
        self.client = get_client()

    def tearDown(self):
        self.stop_test_server()

    def test_getDateTimeField1(self):
        call_command('loaddata', 'small_data.json')
        for i in self.client.inbox_message.objects.all():
            self.assertTrue(isinstance(i.ctime, datetime))

    def test_setDateTimeField1(self):
        ctime = datetime.now()
        utime = datetime.now()
        message = self.client.message(
            subject=id_generator(), body=id_generator(), ctime=ctime, utime=utime)
        message.save()
        self.assertTrue(isinstance(message.ctime, datetime))
        self.assertTrue(isinstance(message.utime, datetime))
#        self.assertTrue(message.ctime == ctime)  # lag
#        self.assertTrue(message.utime == utime)  # lag

        message_ = self.client.message.objects.get(id=message.id)
        self.assertTrue(message.id == message_.id)

    def test_DecimalField1(self):
        pass

    def test_FloatField1(self):
        pass

    def test_IntegerField1(self):
        pass

    def test_GenericIPAddressField(self):
        pass

