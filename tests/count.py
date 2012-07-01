from queryset_client import Client

client = Client("http://192.168.57.132:8888/message/v1/")


def test_count1():
    num = client.inbox_message_many.objects.count()
    assert 0 < num
    assert isinstance(num, int)


def test_count2():
    al = client.inbox_message_many.objects.filter(id__in=xrange(99, 110))
    num = al.count()
    assert 11 == num
    assert isinstance(num, int)