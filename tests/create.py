from queryset_client.client import Client, FieldTypeError


client = Client("http://192.168.57.132:8888/message/v1/")


def test_create1():
    assert True