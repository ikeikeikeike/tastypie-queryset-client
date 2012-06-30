from queryset_client.client import Client, QuerySet

client = Client("http://192.168.57.132:8888/message/v1/")


for i in client.message.objects.order_by("-id"):
    assert i


order =  client.message.objects.all().order_by("-id")
for i in order:
    assert i


for i, k in zip(order.all(), order):
    assert i.id == k.id