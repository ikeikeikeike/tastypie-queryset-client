from queryset_client import Client

client = Client("http://192.168.57.132:8888/message/v1/")


def test_many1():
    from queryset_client.client import QuerySet
    for i in xrange(99, 110):
        many = client.inbox_message_many.objects.get(id=i)
        assert many.inbox_message
        assert isinstance(many.inbox_message.filter(), QuerySet)


def test_many2():
    for i in client.inbox_message_many.objects.filter(id__in=xrange(99, 110)):
        assert i.inbox_message


def test_many3():
    for i in client.inbox_message_many.objects.filter(id__in=xrange(99, 102)):
        assert i.inbox_message.all()


def test_many4():
    for i in client.inbox_message_many.objects.all():
        assert i


