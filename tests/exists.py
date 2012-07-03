from queryset_client.client import Client


client = Client("http://192.168.57.132:8888/message/v1/")


def test_exists1():
    assert client.message.objects.exists() is False
    assert client.message.objects.all().exists() is True
