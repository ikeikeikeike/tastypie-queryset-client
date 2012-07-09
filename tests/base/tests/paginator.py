from django.core.paginator import Paginator
from testcases import (
    TestServerTestCase,
    get_client
)
from .utils import id_generator


class PaginatorTestCase(TestServerTestCase):

    def setUp(self):
        self.start_test_server()
        self.client = get_client()
        for i in xrange(0, 100):
            message = self.client.message()
            message.subject = id_generator()
            message.body = id_generator()
            message.save()

            inbox = self.client.inbox()
            inbox.did = id_generator()
            inbox.save()

            inbox_message = self.client.inbox_message()
            inbox_message.message = message.resource_uri
            inbox_message.inbox = inbox.resource_uri
            inbox_message.save()


    def tearDown(self):
        self.stop_test_server()

    def test_paginator(self):
        message = self.client.message.objects.all()

        p = Paginator(message,25)
        self.assertTrue(p.count)
        self.assertTrue(p.num_pages)
        self.assertTrue(p.page_range)

        page1 = p.page(1)
        self.assertTrue(page1.object_list)

        page2 = p.page(2)
        self.assertTrue(page2.object_list)
        self.assertTrue(page2.has_next())
        self.assertTrue(page2.has_previous())
        self.assertTrue(page2.has_other_pages())
        self.assertTrue(page2.next_page_number())
        self.assertTrue(page2.previous_page_number())
        self.assertTrue(page2.start_index()) # The 1-based index of the first item on this page
        self.assertTrue(page2.end_index()) # The 1-based index of the last item on this page
        #print p.page(0)  # TODO:
        self.assertTrue(p.page(3))