# -*- coding: utf-8 -*-
import copy
import urlparse
import slumber
import exceptions as exc


def urljoin(*args):
    return "{0}&".format(urlparse.urljoin(*args))


class Response(object):

    def __init__(self, model, response):
        self.model = model
        self._response = response
        self._schema = self.model.schema()

    def __repr__(self):
        return "<{0}: {1}>".format(self.model._model_name, self._response)

    def __getattr__(self, attr):
        if not attr in self._response:
            raise AttributeError(attr)

        if not "related_type" in self._schema["fields"][attr]:
            return self._response[attr]

        # TODO: ManyToMany Another Client

        related_type = self._schema["fields"][attr]["related_type"]
        if True:
            # getattr(self.model._client, attr)(1).get()
            return LazyResponse(model=self.model, attr=attr, url=self._response[attr])
#            return # Object
        elif related_type == "to_one":
            return  # Object
        elif related_type == "many":
            return  # Object
        elif related_type == "for":
            return  # Object

    def __getitem__(self, item):
        if item in self._response:
            return self._response[item]
        else:
            raise KeyError(item)

    def __contains__(self, attr):
        return attr in self._response


class LazyResponse(Response):

    # TODO: ManyToMany Another Client
    def __init__(self, attr, url, *args, **kwargs):
        super(LazyResponse, self).__init__(response=None, *args, **kwargs)
        self._attr = attr
        self._url = url
        self.client = getattr(self.model._client, attr)

    def __repr__(self):
        return "<{0}: {1}>".format(self._attr, self._response or self._url)

    def _fetch(self):
        if not self._response:
            id_ = self._url.split("/")[::-1][1]
            self._response = self.client(id_).get()
        return self._response

    def __getattr__(self, *args, **kwargs):
        self._fetch()
        return super(LazyResponse, self).__getattr__(*args, **kwargs)

    def __getitem__(self, *args, **kwargs):
        self._fetch()
        return super(LazyResponse, self).__getattr__(*args, **kwargs)

    def __contains__(self, *args, **kwargs):
        self._fetch()
        return super(LazyResponse, self).__getattr__(*args, **kwargs)


class QuerySet(object):

    def __init__(self, model, responses=None, **kwargs):
        self.model = model
        self._responses = responses
        self._objects = responses and dict(enumerate(responses["objects"]))  # result_cache
        self._meta = responses and responses["meta"]
        self._result_cache = None
        self._kwargs = kwargs
        self._response_class = kwargs.get("response_class", Response)

    def __repr__(self):
        return "<QuerySet {0} ({1}/{2})>".format(
                    self._response_class, self.__len__(), self._meta["total_count"])

    def __len__(self):
        return len(self._objects)

    def __iter__(self):
        index = 0
        klass = copy.deepcopy(self)
        while 1:
            try:
                yield klass._wrap_response(klass._objects[index])
                index += 1
            except KeyError:
                klass = klass._next()
                index = 0

    def _next(self):
        """ request next page """
        if not self._meta["next"]:
            raise StopIteration()
        url = urljoin(self.model._base_url, self._meta["next"])
        return self.__class__(self.model, self.model.client(url_override=url).get())

    def _previous(self):
        """ request previous page """
        if not self._meta["previous"]:
            raise StopIteration()
        url = urljoin(self.model._base_url, self._meta["previous"])
        return self.__class__(self.model, self.model.client(url_override=url).get())

    def __getitem__(self, k):
        # if isinstance(k, slice):
            # qs = self._clone()
            # if k.start is not None:
                # start = int(k.start)
            # else:
                # start = None
            # if k.stop is not None:
                # stop = int(k.stop)
            # else:
                # stop = None
            # qs.query.set_limits(start, stop)
            # return k.step and list(qs)[::k.step] or qs

        try:
            return self._wrap_response(self._objects[k])
        except KeyError  as err:
            raise IndexError(err)

    def _wrap_response(self, dic):
        return self._response_class(self.model, dic)

    def get_pk(self, pk):
        return self._wrap_response(self.model.client(pk).get())

    def get(self, *args, **kwargs):
        clone = self.filter(*args, **kwargs)
        num = len(clone)
        if num > 1:
            raise exc.MultipleObjectsReturned(
                "get() returned more than one {0} -- it returned {1}! Lookup parameters were {2}"
                    .format(self.model._model_name, num, kwargs))
        elif not num:
            raise exc.ObjectDoesNotExist("{0} matching query does not exist."
                    .format(self.model._model_name))
        return clone[0]

    def filter(self, *args, **kwargs):
        return self.__class__(self.model, self.model.client.get(*args, **kwargs))


class Manager(object):

    def __init__(self, model):
        self.model = model

    def get_query_set(self):
        return QuerySet(self.model)

    def all(self):
        return self.get_query_set()

    def count(self):
        return self.get_query_set().count()

    def dates(self, *args, **kwargs):
        return self.get_query_set().dates(*args, **kwargs)

    def distinct(self, *args, **kwargs):
        return self.get_query_set().distinct(*args, **kwargs)

    def extra(self, *args, **kwargs):
        return self.get_query_set().extra(*args, **kwargs)

    def get(self, *args, **kwargs):
        return self.get_query_set().get(*args, **kwargs)

    def get_or_create(self, **kwargs):
        return self.get_query_set().get_or_create(**kwargs)

    def create(self, **kwargs):
        return self.get_query_set().create(**kwargs)

    def bulk_create(self, *args, **kwargs):
        return self.get_query_set().bulk_create(*args, **kwargs)

    def filter(self, *args, **kwargs):
        return self.get_query_set().filter(*args, **kwargs)

    def aggregate(self, *args, **kwargs):
        return self.get_query_set().aggregate(*args, **kwargs)

    def annotate(self, *args, **kwargs):
        return self.get_query_set().annotate(*args, **kwargs)

    def complex_filter(self, *args, **kwargs):
        return self.get_query_set().complex_filter(*args, **kwargs)

    def exclude(self, *args, **kwargs):
        return self.get_query_set().exclude(*args, **kwargs)

    def in_bulk(self, *args, **kwargs):
        return self.get_query_set().in_bulk(*args, **kwargs)

    def iterator(self, *args, **kwargs):
        return self.get_query_set().iterator(*args, **kwargs)

    def latest(self, *args, **kwargs):
        return self.get_query_set().latest(*args, **kwargs)

    def order_by(self, *args, **kwargs):
        return self.get_query_set().order_by(*args, **kwargs)

    def select_for_update(self, *args, **kwargs):
        return self.get_query_set().select_for_update(*args, **kwargs)

    def select_related(self, *args, **kwargs):
        return self.get_query_set().select_related(*args, **kwargs)

    def prefetch_related(self, *args, **kwargs):
        return self.get_query_set().prefetch_related(*args, **kwargs)

    def values(self, *args, **kwargs):
        return self.get_query_set().values(*args, **kwargs)

    def values_list(self, *args, **kwargs):
        return self.get_query_set().values_list(*args, **kwargs)

    def update(self, *args, **kwargs):
        return self.get_query_set().update(*args, **kwargs)

    def reverse(self, *args, **kwargs):
        return self.get_query_set().reverse(*args, **kwargs)

    def defer(self, *args, **kwargs):
        return self.get_query_set().defer(*args, **kwargs)

    def only(self, *args, **kwargs):
        return self.get_query_set().only(*args, **kwargs)

    def using(self, *args, **kwargs):
        return self.get_query_set().using(*args, **kwargs)

    def exists(self, *args, **kwargs):
        return self.get_query_set().exists(*args, **kwargs)


class Model(object):

    def __init__(self, client, model_name, endpoint, schema, objects=None):
        self._client = client
        self._model_name = model_name
        self._endpoint = endpoint
        self._schema = schema
        self.objects = objects or Manager(self)
        self.client = getattr(client, model_name)
        self._schema_data = self.client.schema.get()
        self._base_url = client._store["base_url"]

    def __repr__(self):
        return "<{0}: {1}>".format(self._model_name, self._endpoint)

    def schema(self):
        return self._schema_data

    def save(self):
#        self.client.put(); self.client.post()
        pass

    def delete(self):
#        self.client.delete()
        pass


class Client(object):

    def __init__(self, base_url, auth=None, client=None):
        self._client = (client or slumber.API)(base_url, auth)
        self._method_gen()

    def request(self, url, method="GET"):
        s = self._client._store
        requests = s["session"]
        serializer = slumber.serialize.Serializer(default_format=s["format"])
        return serializer.loads(requests.request(method, url).content)

    def schema(self, url=None):
        return self.request(url or self._client._store["base_url"])

    def _method_gen(self):
        s = self.schema()
        for method_name in s:
            setattr(self, method_name, Model(self._client, method_name,
                        s[method_name]["list_endpoint"], s[method_name]["schema"]))
