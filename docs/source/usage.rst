
Usage
======

Operation like a Django Model API.


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


Filter
-------

::

    >>> client = Client("http://api.server.com/your/v1/")
    >>> client.your.objects.filter(name="your")
    <QuerySet your <type 'type'> (3/3)>

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
    <QuerySet parent <type 'type'> (2/2)>
    >>> for pa in parent:
    .  .  .         print pa.your
    .  .  .
    <your: name>
    <your: name>


