from queryset_client.client import Client


client = Client("http://192.168.57.132:8888/message/v1/")


def test_create1():
    subject = "subject create 1"
    body = "body create 1"
    message = client.message.objects.create(subject=subject, body=body)

    message_ = client.message.objects.get(id=message.id, subject=subject, body=body)
    assert message_.id == message.id
    assert message_.subject == message.subject
    assert message_.body == message.body
