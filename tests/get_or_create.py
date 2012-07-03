from queryset_client.client import (
    Client,
    MultipleObjectsReturned,
    ObjectDoesNotExist
)
from .utils import id_generator

client = Client("http://192.168.57.132:8888/message/v1/")


def test_get_or_create1():
    subject = "subject get_or_create 1 - {0}".format(id_generator())
    body = "body get_or_create 1 - {0}".format(id_generator())

    message, created = client.message.objects.get_or_create(subject=subject, body=body)

    message_ = client.message.objects.get(id=message.id, subject=subject, body=body)
    assert message_.id == message.id
    assert message_.subject == message.subject
    assert message_.body == message.body


def test_get_or_create2():
    subject1 = "subject get_or_create 2 - {0}".format(id_generator())
    body1 = "body get_or_create 2 - {0}".format(id_generator())

    message, created = client.message.objects.get_or_create(subject=subject1, body=body1)

    subject2 = "subject get_or_create 2 update"
    body2 = "body get_or_create 2 update"
    message.subject = subject2
    message.body = body2
    message.save()
    try:
        client.message.objects.get(id=message.id, subject=subject1, body=body1)
    except ObjectDoesNotExist:
        assert True
    else:
        assert False

    try:
        message_ = client.message.objects.get(id=message.id, subject=subject2, body=body2)
    except ObjectDoesNotExist:
        assert False
    else:
        assert True
        assert message_.id == message.id
        assert message_.subject == message.subject
        assert message_.body == message.body


def test_get_or_create3():
    subject1 = "subject get_or_create 3 - {0}".format(id_generator())
    body1 = "body get_or_create 3 - {0}".format(id_generator())

    message = client.message(subject=subject1, body=body1)
    message.save()

    message_, created = client.message.objects.get_or_create(subject=subject1, body=body1)
    assert message_.id == message.id
    assert message_.subject == message.subject == subject1
    assert message_.body == message.body == body1


def test_get_or_create4():
    subject1 = "subject get_or_create 4"
    body1 = "body get_or_create 4"

    message = client.message(subject=subject1, body=body1)
    message.save()

    message = client.message(subject=subject1, body=body1)
    message.save()

    try:
        client.message.objects.get_or_create(subject=subject1, body=body1)
    except MultipleObjectsReturned:
        assert True
    else:
        assert False

