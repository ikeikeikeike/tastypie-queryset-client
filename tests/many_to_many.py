from queryset_client import Client

client = Client("http://192.168.57.132:8888/message/v1/")

for i in xrange(99, 110):
    many = client.inbox_message_many.objects.get(id=i)
    print many.inbox_message
    print many.inbox_message.filter()

for i in client.inbox_message_many.objects.filter(id__in=xrange(99, 110)):
    print i.inbox_message

for i in client.inbox_message_many.objects.filter(id__in=xrange(99, 102)):
    print i.inbox_message.all()

for i in client.inbox_message_many.objects.all():
    print i


