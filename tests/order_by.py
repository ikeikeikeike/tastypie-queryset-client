from queryset_client import Client

client = Client("http://192.168.57.132:8888/message/v1/")


def test_order1():
    for i in client.message.objects.order_by("-id")[0:30]:
        assert i


def test_order2():
    order =  client.message.objects.all().order_by("-id")[0:30]
    for i in order:
        assert i


def test_order3():
    order =  client.message.objects.all().order_by("-id")
    for i, k in zip(order.all(), order):
        assert i.id == k.id


def test_order4():
    order =  client.message.objects.order_by("-id")
    for i, k in zip(order.all(), order):
        assert i.id == k.id