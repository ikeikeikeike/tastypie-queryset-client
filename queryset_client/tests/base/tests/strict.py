# from decimal import Decimal
from datetime import datetime
#from django.conf import settings
#settings.DEBUG = True
from testcases import (
    TestServerTestCase,
    get_client
)
from django.core.management import call_command
from .utils import id_generator


def _getDateTimeField(klass):
    call_command('loaddata', 'small_data.json')
    for i in klass.client.inbox_message.objects.all():
        klass.assertTrue(isinstance(i.ctime, datetime))


def _setDateTimeField(klass):
    ctime = datetime.now()
    utime = datetime.now()
    message = klass.client.message(
        subject=id_generator(), body=id_generator(), ctime=ctime, utime=utime)
    message.save()
    klass.assertTrue(isinstance(message.ctime, datetime))
    klass.assertTrue(isinstance(message.utime, datetime))
#        klass.assertTrue(message.ctime == ctime)  # lag
#        klass.assertTrue(message.utime == utime)  # lag

    message_ = klass.client.message.objects.get(id=message.id)
    klass.assertTrue(message.id == message_.id)

# def _DecimalField(klass):
    # decimal_test = Decimal('0.2')

    # # Test save
    # strict = klass.client.strict(decimal_test=decimal_test)
    # strict.save()

    # # Tests
    # klass.assertTrue(isinstance(strict.decimal_test, decimal_test))
    # klass.assertTrue(strict.decimal_test == decimal_test)

    # # Get
    # strict_ = klass.client.strict.objects.get(id=strict.id)
    # klass.assertTrue(strict.id == strict_.id)

    # # Search
    # strict_ = klass.client.strict.objects.filter(decimal_test=decimal_test)
    # klass.assertTrue(strict_.count() == 1)


def _FloatField(klass):
    float_test = float(0.2)

    # Test save
    strict = klass.client.strict(float_test=float_test)
    strict.save()

    # Tests
    klass.assertTrue(isinstance(strict.float_test, float))
    klass.assertTrue(strict.float_test == float_test)

    # Get
    strict_ = klass.client.strict.objects.get(id=strict.id)
    klass.assertTrue(strict.id == strict_.id)

    # Search
    strict_ = klass.client.strict.objects.filter(float_test=float_test)
    klass.assertTrue(strict_.count() == 1)


def _IntegerField(klass):
    integer_test = 10

    # Test save
    strict = klass.client.strict(integer_test=integer_test)
    strict.save()

    # Tests
    klass.assertTrue(isinstance(strict.integer_test, int))
    klass.assertTrue(strict.integer_test == integer_test)

    # Get
    strict_ = klass.client.strict.objects.get(id=strict.id)
    klass.assertTrue(strict.id == strict_.id)

    # Search
    strict_ = klass.client.strict.objects.filter(integer_test=integer_test)
    klass.assertTrue(strict_.count() == 1)


def _BooleanField(klass):
    pass


def _GenericIPAddressField(klass):
    pass


class StrictTestCase(TestServerTestCase):

    def setUp(self):
        self.start_test_server()
        self.client = get_client()

    def tearDown(self):
        self.stop_test_server()

    def test_getDateTimeField(self):
        _getDateTimeField(self)

    def test_setDateTimeField(self):
        _setDateTimeField(self)

    # def test_DecimalField(self):
        #_DecimalField(self)

    def test_FloatField(self):
        _FloatField(self)

    def test_IntegerField(self):
        _IntegerField(self)

    def test_BooleanField(self):
        _BooleanField(self)

    def test_GenericIPAddressField(self):
        _GenericIPAddressField(self)


class StrictTestCase(TestServerTestCase):

    def setUp(self):
        self.start_test_server()
        self.client = get_client(strict_field=False)

    def tearDown(self):
        self.stop_test_server()

    def test_getDateTimeField(self):
        _getDateTimeField(self)

    def test_setDateTimeField(self):
        _setDateTimeField(self)

    # def test_DecimalField(self):
        #_DecimalField(self)

    def test_FloatField(self):
        _FloatField(self)

    def test_IntegerField(self):
        _IntegerField(self)

    def test_BooleanField(self):
        _BooleanField(self)

    def test_GenericIPAddressField(self):
        _GenericIPAddressField(self)
