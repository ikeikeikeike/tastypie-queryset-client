#from slumber.exceptions import HttpClientError
from queryset_client.client import Client, FieldTypeError, ObjectDoesNotExist
from .utils import id_generator


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
    subject = "subject call 1"
    body = "body call 1"
    message_obj = client.message(subject=subject, body=body)
    assert message_obj.subject == subject
    assert message_obj.body == body


def test_call2():
    try:
        client.message(errorfield="oha yo! oha yo!")
    except FieldTypeError:
        assert True
    else:
        assert False


def test_save1():
    """ (new) """
    subject = "subject save 1"
    body = "body save 1"
    message = client.message(subject=subject, body=body)
    message.save()

    message_ = client.message.objects.get(id=message.id, subject=subject, body=body)
    assert message_.id == message.id
    assert message_.subject == message.subject
    assert message_.body == message.body


def test_save2():
    """ (update) """
    subject1 = "subject save 2"
    body1 = "body save 2"
    message = client.message(subject=subject1, body=body1)
    message.save()

    subject2 = "subject save 2 update"
    body2 = "body save 2 update"
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


def test_save3():
    """ (update) for query_set """

    subject = id_generator()
    body = id_generator()

    for message in client.message.objects.filter(id__in=xrange(20, 33)):
        message.subject = subject
        message.body = body
        message.save()

    for message in client.message.objects.filter(id__in=xrange(20, 33)):
        assert message.subject == subject
        assert message.body == body


def test_save_rel1():
    """ relation """
#    subject = ""
#    body = ""
#    message = client.inbox_message(subject=subject, body=body)
#    message.save()


def test_save_many1():
    """ many to many """
#    subject = ""
#    body = ""
#    message = client.inbox_message_many(inbox_message=inbox_message)
#    message.save()


def test_delete1():
    subject = "subject delete 1"
    body = "body delete 1"
    message = client.message(subject=subject, body=body)
    message.save()

    message_ = client.message.objects.get(id=message.id, subject=subject, body=body)
    assert message_.id == message.id
    assert message_.subject == message.subject
    assert message_.body == message.body

    message.delete()
    try:
        message.id
    except AttributeError:
        assert True
    else:
        assert False

    try:
        message_.delete()
    except Exception:
        assert True
    else:
        assert False
    try:
        message.id
    except AttributeError:
        assert True
    else:
        assert False
