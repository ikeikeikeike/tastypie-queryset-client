from queryset_client import Client

client = Client("http://192.168.57.132:8888/message/v1/")

# TODO: input prepend data
def test_lazy1():
    fl = client.inbox_message_many.objects.filter()
    if 0 < len(fl):
        assert fl
        for f in fl:
            assert f