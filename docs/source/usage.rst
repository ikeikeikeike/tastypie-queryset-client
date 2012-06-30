
Usage
======

Client for Tastypie. Provide operation similar to the Django Model API.

Schema
-------

::

    client = Client("http://api.server.com/your/v1/")
    client.schema()


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


Filter
-------

::

    >>> client = Client("http://api.server.com/your/v1/")
    >>> client.your.objects.filter(name="your")
    <QuerySet <class 'Response'> (3/3)>


Save
-----

::

    >>> client = Client("http://api.server.com/your/v1/")
    >>> your = client.your(name="name")
    >>> your
    <your: {u"id": u"2", u"name": u"name"}>
    >>> your.save()  # save Your object.


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
