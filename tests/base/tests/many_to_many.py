from django.conf import settings
settings.DEBUG = True
from testcases import (
    TestServerTestCase,
    get_client
)
from django.core.management import call_command
from queryset_client.client import (
    ObjectDoesNotExist,
    QuerySet,
    ManyToManyManager,
    Response
)


class ManyToManyTestCase(TestServerTestCase):

    def setUp(self):
        self.start_test_server()
        self.client = get_client()
        call_command('loaddata', 'base_data.json')

    def tearDown(self):
        self.stop_test_server()

    def test_many1(self):
        for ran in range(90, 130):
            try:
                many = self.client.inbox_message_many.objects.get(id=ran)
                self.assertTrue(many.inbox_message)
                self.assertTrue(isinstance(many.inbox_message.filter(), QuerySet))
            except ObjectDoesNotExist, err:
                self.assertTrue(True)

        nums = range(60, 80)
        for m1, num in zip(self.client.inbox_message_many.objects.filter(id__in=nums), nums):
            self.assertTrue(isinstance(m1.inbox_message, ManyToManyManager))
            self.assertTrue(m1.id == num)

    def test_many2(self):
        nums = range(5, 30)
        many1 = self.client.inbox_message_many.objects.filter(id__in=nums)
        many2 = self.client.inbox_message_many.objects.filter(id__in=nums)

        for m in many1:
            self.assertTrue(isinstance(m.inbox_message, ManyToManyManager))
        for m in many2:
            self.assertTrue(isinstance(m.inbox_message, ManyToManyManager))
        for m in many1:
            self.assertTrue(isinstance(m.id, int))
        for m in many2:
            self.assertTrue(isinstance(m.id, int))

        for m1, m2 in zip(many1, many2):
            self.assertTrue(m1.inbox_message.all().count() == m2.inbox_message.all().count())
            self.assertTrue(m1.id == m2.id)

        qs1 = self.client.inbox_message.objects.filter(id__in=nums)
        for i, k in zip(self.client.inbox_message_many.objects.filter(id__in=nums), many1):
            self.assertTrue(i.inbox_message.all())
            self.assertTrue(i.id == k.id)

            qs = i.inbox_message.filter()
            for inbox_message in qs:
                self.assertTrue(hasattr(inbox_message, "read"))
                self.assertTrue(isinstance(inbox_message.message, Response))
                self.assertTrue(isinstance(inbox_message.inbox, Response))
                self.assertTrue(inbox_message.message.subject)
                self.assertTrue(inbox_message.inbox.did)

            self.assertTrue(qs1.count() != qs.count())
