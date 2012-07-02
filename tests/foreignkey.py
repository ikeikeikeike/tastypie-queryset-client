from queryset_client import Client


client = Client("http://192.168.57.132:8888/message/v1/")


# TODO: input prepend data
def test_foreignkey1():

    if 0 < client.inbox_message.objects.count():
        assert client.inbox_message.objects.all()[0].message.id
        assert client.inbox_message.objects.all()[1].message.id
        assert  client.inbox_message.objects.all()[2].message.id

    try:
        client.inbox_message.objects.all()[99999]
    except IndexError:
        assert True
    else:
        assert False




