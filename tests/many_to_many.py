from queryset_client.client import Client, QuerySet

client = Client("http://192.168.57.132:8888/message/v1/")

for i in xrange(99, 110):
    many = client.inbox_message_many.objects.get(id=i)
    assert many.inbox_message
    assert isinstance(many.inbox_message.filter(), QuerySet)

for i in client.inbox_message_many.objects.filter(id__in=xrange(99, 110)):
    assert i.inbox_message

for i in client.inbox_message_many.objects.filter(id__in=xrange(99, 102)):
    assert i.inbox_message.all()

for i in client.inbox_message_many.objects.all():
    assert i


