from django.core.management import call_command
from django.core.paginator import Paginator
from testcases import (
    TestServerTestCase,
    get_client
)
from queryset_client.client import QuerySet

class PaginatorTestCase(TestServerTestCase):

    def setUp(self):
        self.start_test_server()
        self.client = get_client()
        call_command('loaddata', 'base_data.json')

    def tearDown(self):
        self.stop_test_server()

    def test_paginator(self):
        message = self.client.message.objects.all()

        p = Paginator(message, 100)
        self.assertTrue(p.count == 246)
        self.assertTrue(p.num_pages == 3)
        self.assertTrue(p.page_range == [1, 2, 3])

        page1 = p.page(1)
        self.assertTrue(isinstance(page1.object_list, QuerySet))
        self.assertTrue(page1.has_next() == True)
        self.assertTrue(page1.has_previous() == False)
        self.assertTrue(page1.has_other_pages() == True)
        self.assertTrue(page1.next_page_number() == 2)
        self.assertTrue(page1.previous_page_number() == 0)
        self.assertTrue(page1.start_index() == 1)
        self.assertTrue(page1.end_index() == 100)

        page2 = p.page(2)
        self.assertTrue(isinstance(page2.object_list, QuerySet))
        self.assertTrue(page2.has_next() == True)
        self.assertTrue(page2.has_previous() == True)
        self.assertTrue(page2.has_other_pages() == True)
        self.assertTrue(page2.next_page_number() == 3)
        self.assertTrue(page2.previous_page_number() == 1)
        self.assertTrue(page2.start_index() == 101)
        self.assertTrue(page2.end_index() == 200)

        page3 = p.page(3)
        self.assertTrue(isinstance(page3.object_list, QuerySet))
        self.assertTrue(page3.has_next() == False)
        self.assertTrue(page3.has_previous() == True)
        self.assertTrue(page3.has_other_pages() == True)
        self.assertTrue(page3.next_page_number() == 4)
        self.assertTrue(page3.previous_page_number() == 2)
        self.assertTrue(page3.start_index() == 201)
        self.assertTrue(page3.end_index() == 246)

        num = 0
        for num, i in enumerate(page1.object_list):
            print num, i
            pass
        self.assertTrue(num == 99)

        num = 0
        for num, i in enumerate(page2.object_list):
            print num, i
            pass
        self.assertTrue(num == 99)

        num = 0
        for num, i in enumerate(page3.object_list):
            print num, i
            pass
        self.assertTrue(num == 45)