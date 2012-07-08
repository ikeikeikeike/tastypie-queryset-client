from queryset_client.client import Client


client = Client("http://192.168.57.132:8888/message/v1/")


def test_len1():
    message = client.message.objects.all()
    assert len(message) == client.message.objects.count()


def test_len2():
    message = client.message.objects.all()
    assert len(message) == client.message.objects.all().count()