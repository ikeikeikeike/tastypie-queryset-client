from queryset_client import Client

client = Client("http://192.168.57.132:8888/message/v1/")

def test_lazy1():
    fl = client.inbox_message_many.objects.filter()
    assert fl
    for f in fl:
        assert f