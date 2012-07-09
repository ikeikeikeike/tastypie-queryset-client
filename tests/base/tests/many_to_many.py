from testcases import (
    TestServerTestCase,
    get_client
)
from queryset_client.client import (
    ObjectDoesNotExist,
    QuerySet
)


class ManyToManyTestCase(TestServerTestCase):

    def setUp(self):
        self.start_test_server()
        self.client = get_client()

    def tearDown(self):
        self.stop_test_server()

    def test_many1(self):
        for i in xrange(99, 110):
            try:
                many = self.client.inbox_message_many.objects.get(id=i)
                self.assertTrue(many.inbox_message)
                self.assertTrue(isinstance(many.inbox_message.filter(), QuerySet))
            except ObjectDoesNotExist, err:
                self.assertTrue(True)

    def test_many2(self):
        nums = xrange(99, 110)
        for i, num in zip(self.client.inbox_message_many.objects.filter(id__in=nums), nums):
            self.assertTrue(i.inbox_message)
            self.assertTrue(i.id == num)


    def test_many3(self):
        nums = xrange(99, 102)
        for i, num in zip(self.client.inbox_message_many.objects.filter(id__in=nums), nums):
            self.assertTrue(i.inbox_message.all())
            self.assertTrue(i.id == num)


    def test_many4(self):
        for i in self.client.inbox_message_many.objects.all():
            self.assertTrue(i)


