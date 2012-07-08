from queryset_client.client import Client


client = Client("http://192.168.57.132:8888/message/v1/")


def test_exists1():
    message = client.message.objects.exists()
    assert message is True
    message = client.message.objects.all().exists()
    assert message is True
    message = client.message.objects.filter(id=10000000)
    exists = message.exists()
    assert exists is False
