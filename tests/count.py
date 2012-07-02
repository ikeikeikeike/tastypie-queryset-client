from queryset_client import Client

client = Client("http://192.168.57.132:8888/message/v1/")


def test_count1():
    num = client.inbox_message_many.objects.count()
    assert -1 < num
    assert isinstance(num, int)

# TODO: load prepend data
def test_count2():
    nums = client.inbox_message_many.objects.filter(id__in=xrange(0, 12))
    num = nums.count()
    assert 11 == num
    assert isinstance(num, int)