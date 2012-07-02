from queryset_client.client import Client, ObjectDoesNotExist

client = Client("http://192.168.57.132:8888/message/v1/")


def test_many1():
    from queryset_client.client import QuerySet

    for i in xrange(99, 110):
        try:
            many = client.inbox_message_many.objects.get(id=i)
            assert many.inbox_message
            assert isinstance(many.inbox_message.filter(), QuerySet)
        except ObjectDoesNotExist, err:
            assert True


def test_many2():
    nums = xrange(99, 110)
    for i, num in zip(client.inbox_message_many.objects.filter(id__in=nums), nums):
        assert i.inbox_message
        assert i.id == num


def test_many3():
    nums = xrange(99, 102)
    for i, num in zip(client.inbox_message_many.objects.filter(id__in=nums), nums):
        assert i.inbox_message.all()
        assert i.id == num


def test_many4():
    for i in client.inbox_message_many.objects.all():
        assert i


