
Usage
======

Client for Tastypie. Provide operation similar to the Django Model API.

Schema
-------

::

    # base schema
    client = Client("http://api.server.com/your/v1/")
    client.schema()

    # model schema
    client.your.schema()
    client.message.schema()

Get
----

::

    >>> client = Client("http://api.server.com/your/v1/")
    >>> client.your.objects.get(name="your")
    <your: {u"id": u"1", u"name": u"your", u"status": u"any"}>


Count
------

::

    >>> client = Client("http://api.server.com/your/v1/")
    >>> client.your.objects.count()
    100


Exists
-------

::

    >>> client = Client("http://api.server.com/your/v1/")
    >>> client.your.objects.exists()
    False
    >>> queryset = client.your.objects.all()
    >>> queryset.exists()
    True


Filter
-------

::

    >>> client = Client("http://api.server.com/your/v1/")
    >>> client.your.objects.filter(name="your")
    <QuerySet <class 'Response'> (3/3)>


Order By
---------

::

    >>> client = Client("http://api.server.com/your/v1/")
    >>> order = []
    >>> for p in client.your.objects.order_by("-id"):
    .  .  .         order.append(p)
    .  .  .         print p.your
    .  .  .
    <your: {u"id": u"3", u"name": u"name3"}>
    <your: {u"id": u"2", u"name": u"name2"}>
    <your: {u"id": u"1", u"name": u"name1"}>
    >>> for i, k in zip(client.your.objects.order_by("-id"), order):
    .  .  .         print i.id == k.id
    .  .  .
    True
    True
    True


Relation
---------

::

    >>> client = Client("http://api.server.com/your/v1/")
    >>> parent = client.parent.objects.filter(parent__your__name="name")
    >>> parent
    <QuerySet <class 'Response'> (2/2)>
    >>> for p in parent:
    .  .  .         print p.your
    .  .  .
    <your: {u"id": u"1", u"name": u"name", u"status": u"any"}>
    <your: {u"id": u"2", u"name": u"name", u"status": u"any"}>


ManyToMany
~~~~~~~~~~~~

::

    >>> client = Client("http://api.server.com/your/v1/")
    >>> parent = client.parent.objects.filter(id__in=[109, 110, 111])
    >>> parent
    <QuerySet <class 'Response'> (3/3)>
    >>> for p in parent:
    .  .  .         print p
    .  .  .
    <your: {u"id": u"109", u"name": u"name109", u"status": u"any"}>
    <your: {u"id": u"110", u"name": u"name110", u"status": u"any"}>
    <your: {u"id": u"111", u"name": u"name111", u"status": u"any"}>
    >>> for p in parent:
    .  .  .         print p.your
    .  .  .
    <ManyToManyManager object at 0x10a12e510>
    <ManyToManyManager object at 0x10a12e510>
    <ManyToManyManager object at 0x10a12e510>
    >>> for p in parent:
    .  .  .         print p.your.all()
    .  .  .
    <QuerySet <class 'Response'> (1/1)>
    <QuerySet <class 'Response'> (10/10)>
    <QuerySet <class 'Response'> (20/25)>


Save
-----

::

    >>> client = Client("http://api.server.com/your/v1/")
    >>> your = client.your(name="name")
    >>> your
    <your: {u"name": u"name"}>
    >>> your.save()  # save Your object.
    >>> your
    <your: {u"id": u"2", u"name": u"name"}>

Create
~~~~~~~

::

    >>> client = Client("http://api.server.com/your/v1/")
    >>> your = client.your.objects.create(name="name")
    >>> your
    <your: {u"id": u"2", u"name": u"name"}>


Get OR Create
~~~~~~~~~~~~~~~

Returns a tuple of (object, created)

::

    >>> client = Client("http://api.server.com/your/v1/")
    >>> client.your.objects.get_or_create(name="name")
    (<your: {u"id": u"2", u"name": u"name"}>, True)
    >>> client.your.objects.get_or_create(name="name")
    (<your: {u"id": u"2", u"name": u"name"}>, False)


Field
~~~~~~

::

    >>> client = Client("http://api.server.com/your/v1/")
    >>> your = client.your
    >>> your
    <your: /your/v1/your/>
    >>> you = your(name="your")
    >>> you.bankcode = 4649
    <your: /your/v1/your/ {'name': 'your', 'bankcode': 4649}>
    >>> you.name
    'your'
    >>> you.bankcode
    4649
    >>> your.save()  # save Your object.


Delete
--------

::

    >>> client = Client("http://api.server.com/your/v1/")
    >>> message = client.message(subject="subject delete 1", body="body delete 1")
    >>> message.save()
    >>> message.id
    <message: {u"id": u"1", u"subject": u"subject delete 1", u"body": u"body delete 1"}>
    >>> message.delete()  # remove Message object.
    >>> try:
    >>>     message.id
    >>> except AttributeError:
    >>>     assert True  # throw AttributeError.

