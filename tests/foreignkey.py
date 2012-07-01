from queryset_client import Client


client = Client("http://192.168.57.132:8888/message/v1/")


def test_foreignkey1():
    a = client.inbox_message.objects.all()[0]
    b = client.inbox_message.objects.all()[1]
    c = client.inbox_message.objects.all()[2]
    assert a.id
    assert b.id
    assert c.id

    message_id1 = a.message.id
    message_id2 = b.message.id
    message_id3 = c.message.id



