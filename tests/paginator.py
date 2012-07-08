from queryset_client.client import Client
from django.core.paginator import Paginator


client = Client("http://192.168.57.132:8888/message/v1/")

def test_paginator():
    message = client.message.objects.all()

    p = Paginator(message, 10)
    assert p.count
    assert p.num_pages
    assert p.page_range

    page1 = p.page(1)
    assert page1.object_list

    page2 = p.page(2)
    assert page2.object_list
    assert page2.has_next()
    assert page2.has_previous()
    assert page2.has_other_pages()
    assert page2.next_page_number()
    assert page2.previous_page_number()
    assert page2.start_index() # The 1-based index of the first item on this page
    assert page2.end_index() # The 1-based index of the last item on this page
    #print p.page(0)  # TODO:
    assert p.page(3)