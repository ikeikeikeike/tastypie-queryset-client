from decimal import Decimal
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

    def test_getDateTimeField(self):
        call_command('loaddata', 'small_data.json')
        for i in self.client.inbox_message.objects.all():
            self.assertTrue(isinstance(i.ctime, datetime))

    def test_setDateTimeField(self):
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

    # def test_DecimalField(self):
        # decimal_test = Decimal('0.2')

        # # Test save
        # strict = self.client.strict(decimal_test=decimal_test)
        # strict.save()

        # # Tests
        # self.assertTrue(isinstance(strict.decimal_test, decimal_test))
        # self.assertTrue(strict.decimal_test == decimal_test)

        # # Get
        # strict_ = self.client.strict.objects.get(id=strict.id)
        # self.assertTrue(strict.id == strict_.id)

        # # Search
        # strict_ = self.client.strict.objects.filter(decimal_test=decimal_test)
        # self.assertTrue(strict_.count() == 1)

    def test_FloatField(self):
        float_test = float(0.2)

        # Test save
        strict = self.client.strict(float_test=float_test)
        strict.save()

        # Tests
        self.assertTrue(isinstance(strict.float_test, float))
        self.assertTrue(strict.float_test == float_test)

        # Get
        strict_ = self.client.strict.objects.get(id=strict.id)
        self.assertTrue(strict.id == strict_.id)

        # Search
        strict_ = self.client.strict.objects.filter(float_test=float_test)
        self.assertTrue(strict_.count() == 1)

    def test_IntegerField(self):
        integer_test = 10

        # Test save
        strict = self.client.strict(integer_test=integer_test)
        strict.save()

        # Tests
        self.assertTrue(isinstance(strict.integer_test, int))
        self.assertTrue(strict.integer_test == integer_test)

        # Get
        strict_ = self.client.strict.objects.get(id=strict.id)
        self.assertTrue(strict.id == strict_.id)

        # Search
        strict_ = self.client.strict.objects.filter(integer_test=integer_test)
        self.assertTrue(strict_.count() == 1)

    def test_BooleanField(self):
        pass

    def test_GenericIPAddressField(self):
        pass
