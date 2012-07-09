from django.core.paginator import Paginator
from testcases import (
    TestServerTestCase,
    get_client
)


class PaginatorTestCase(TestServerTestCase):

    def setUp(self):
        self.start_test_server()
        self.client = get_client()

    def tearDown(self):
        self.stop_test_server()

    def test_paginator(self):
        message = self.client.message.objects.all()

        p = Paginator(message, 10)
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