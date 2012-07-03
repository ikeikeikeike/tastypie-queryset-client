from queryset_client import Client


client = Client("http://192.168.57.132:8888/message/v1/")


def test_latest1():
    latest = client.message.objects.latest("id")
    order = client.message.objects.order_by("-id")[0]
    assert latest.id == order.id
