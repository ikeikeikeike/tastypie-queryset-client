from queryset_client.client import Client, FieldTypeError


client = Client("http://192.168.57.132:8888/message/v1/")


def test_type1():
    value = 1
    client.message.id = value
    assert client.message.id == value
    assert client.message._fields["id"] == value


def test_type2():
    value = 1
    try:
        client.message.subject = value
    except FieldTypeError:
        assert True
    else:
        assert False


def test_call1():
    pass


def test_call2():
    pass