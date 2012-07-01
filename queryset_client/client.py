# -*- coding: utf-8 -*-
from datetime import datetime
import copy
import urlparse
import slumber


__all__ = ["Client"]


class ObjectDoesNotExist(Exception):
    pass


class MultipleObjectsReturned(Exception):
    pass


class FieldTypeError(Exception):
    pass


def urljoin(*args):
    return "{0}&".format(urlparse.urljoin(*args))


def parse_id(resouce_uri):
    return resouce_uri.split("/")[::-1][1]


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

        related_type = self._schema["fields"][attr]["related_type"]
        if related_type == "to_many":
            return ManyToManyManager(model=self.model,
                            query={"id__in": [parse_id(url) for url in self._response[attr]]})
        elif related_type == "to_one":
            return LazyResponse(model=self.model, attr=attr, url=self._response[attr])

    def __getitem__(self, item):
        if item in self._response:
            return self._response[item]
        else:
            raise KeyError(item)

    def __contains__(self, attr):
        return attr in self._response


class LazyResponse(Response):

    def __init__(self, attr, url, *args, **kwargs):
        super(LazyResponse, self).__init__(response=None, *args, **kwargs)
        self._attr = attr
        self._url = url
        self.client = getattr(self.model._client, attr)

    def __repr__(self):
        return "<{0}: {1}>".format(self._attr, self._response or self._url)

    def _fetch(self):
        if not self._response:
            self._response = self.client(parse_id(self._url)).get()
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
        self._meta = responses["meta"] if responses else {"total_count": 0}
        self._objects = dict(enumerate(responses["objects"])) if responses else []
        self._result_cache = None
        self._kwargs = kwargs
        self._response_class = kwargs.get("response_class", Response)
        self._query = kwargs.get("query", dict())

    def __repr__(self):
        return "<QuerySet {0} ({1}/{2})>".format(
                    self._response_class, self.__len__(), self._meta["total_count"])

    def __len__(self):
        return len(self._objects)

    def __iter__(self):
        if 1 > self.__len__():
            raise StopIteration()
        index = 0
        klass = copy.deepcopy(self)
        while 1:
            try:
                yield klass._wrap_response(klass._objects[index])
                index += 1
            except KeyError:
                klass = klass._next()
                index = 0

    def _clone(self, responses=None, klass=None, **kwargs):
        if klass is None:
            klass = self.__class__
        kls = klass(model=self.model, responses=responses)
        kls.__dict__.update(kwargs)
        return kls

    def _next(self):
        """ request next page """
        if not self._meta["next"]:
            raise StopIteration()
        url = urljoin(self.model._base_url, self._meta["next"])
        return self._clone(self.model.client(url_override=url).get())

    def _previous(self):
        """ request previous page """
        if not self._meta["previous"]:
            raise StopIteration()
        url = urljoin(self.model._base_url, self._meta["previous"])
        return self._clone(self.model.client(url_override=url).get())

    def __getitem__(self, index):
        try:
            if isinstance(index, slice):
                start = index.start
                step = index.step
                stop = index.stop
                # TODO: slice QuerySet
                return [self._wrap_response(self._objects[i]) for i in range(start, stop)]
            else:
                return self._wrap_response(self._objects[index])
        except KeyError as err:
            raise IndexError(err)

    def _wrap_response(self, dic):
        return self._response_class(self.model, dic)

    def get_pk(self, pk):
        return self._wrap_response(self.model.client(pk).get())

    def get(self, *args, **kwargs):
        clone = self.filter(*args, **kwargs)
        num = len(clone)
        if num > 1:
            raise MultipleObjectsReturned(
                "get() returned more than one {0} -- it returned {1}! Lookup parameters were {2}"
                    .format(self.model._model_name, num, kwargs))
        elif not num:
            raise ObjectDoesNotExist("{0} matching query does not exist."
                    .format(self.model._model_name))
        return clone[0]

    def filter(self, *args, **kwargs):
        return self._filter(*args, **kwargs)

    def _filter(self, *args, **kwargs):

        # TODO: ↓↓↓ ManyToManyで 一件も relationがない場合の処理, 現状元のQuerySetの結果が返される ↓↓↓↓
        # <QuerySet <class 'queryset_client.client.Response'> (0/0)>

        kwargs_ = dict(self._query.items() + kwargs.items())
        clone = self._clone(self.model.client.get(**kwargs_))
        clone._query.update({
            "id__in": [parse_id(klass.resource_uri) for klass in clone[0:len(clone)]]
        })
        return clone

    def count(self):
        if self._objects:
            return self._meta["total_count"]
        return self.filter()._meta["total_count"]

    def all(self):
        return self.filter()

    def order_by(self, *args, **kwargs):

        # TODO: multiple order_by = "order_by=-body&order_by=id"

        order = {"order_by": args[0]}
        clone = self._filter(*args, **dict(order.items() + kwargs.items()))
        clone._query.update(order)
        return clone


class Manager(object):

    def __init__(self, model):
        self.model = model

    def get_query_set(self):
        return QuerySet(self.model)

    def all(self):
        # TODO: return self.get_query_set()
        return self.get_query_set().all()

    def count(self):
        return self.get_query_set().count()

#    def dates(self, *args, **kwargs):
#        return self.get_query_set().dates(*args, **kwargs)

#    def distinct(self, *args, **kwargs):
#        return self.get_query_set().distinct(*args, **kwargs)

#    def extra(self, *args, **kwargs):
#        return self.get_query_set().extra(*args, **kwargs)

    def get(self, *args, **kwargs):
        return self.get_query_set().get(*args, **kwargs)

#    TODO: next implementation
#    def get_or_create(self, **kwargs):
#        return self.get_query_set().get_or_create(**kwargs)

    def create(self, **kwargs):
        return self.get_query_set().create(**kwargs)

#    def bulk_create(self, *args, **kwargs):
#        return self.get_query_set().bulk_create(*args, **kwargs)

    def filter(self, *args, **kwargs):
        return self.get_query_set().filter(*args, **kwargs)

#    def aggregate(self, *args, **kwargs):
#        return self.get_query_set().aggregate(*args, **kwargs)

#    def annotate(self, *args, **kwargs):
#        return self.get_query_set().annotate(*args, **kwargs)

#    def complex_filter(self, *args, **kwargs):
#        return self.get_query_set().complex_filter(*args, **kwargs)

#    def exclude(self, *args, **kwargs):
#        return self.get_query_set().exclude(*args, **kwargs)

#    def in_bulk(self, *args, **kwargs):
#        return self.get_query_set().in_bulk(*args, **kwargs)

#    def iterator(self, *args, **kwargs):
#        return self.get_query_set().iterator(*args, **kwargs)

#    TODO: next implementation
#    def latest(self, *args, **kwargs):
#        return self.get_query_set().latest(*args, **kwargs)

    def order_by(self, *args, **kwargs):
        return self.get_query_set().order_by(*args, **kwargs)

#    def select_for_update(self, *args, **kwargs):
#        return self.get_query_set().select_for_update(*args, **kwargs)

#    TODO: next implementation
#    def select_related(self, *args, **kwargs):
#        return self.get_query_set().select_related(*args, **kwargs)

#    def prefetch_related(self, *args, **kwargs):
#        return self.get_query_set().prefetch_related(*args, **kwargs)

#    TODO: next implementation
#    def values(self, *args, **kwargs):
#        return self.get_query_set().values(*args, **kwargs)

#    TODO: next implementation
#    def values_list(self, *args, **kwargs):
#        return self.get_query_set().values_list(*args, **kwargs)

#    def update(self, *args, **kwargs):
#        return self.get_query_set().update(*args, **kwargs)
#
#    def reverse(self, *args, **kwargs):
#        return self.get_query_set().reverse(*args, **kwargs)
#
#    def defer(self, *args, **kwargs):
#        return self.get_query_set().defer(*args, **kwargs)

#    def only(self, *args, **kwargs):
#        return self.get_query_set().only(*args, **kwargs)

#    def using(self, *args, **kwargs):
#        return self.get_query_set().using(*args, **kwargs)

#    TODO: next implementation
#    def exists(self, *args, **kwargs):
#        return self.get_query_set().exists(*args, **kwargs)

class ManyToManyManager(Manager):

    def __init__(self, query, **kwargs):
        super(ManyToManyManager, self).__init__(**kwargs)
        self._query = query

    def get_query_set(self):
        return QuerySet(self.model, query=self._query)


class Model(object):

    def __init__(self, client, model_name, endpoint, schema, objects=None):
        self.client = getattr(client, model_name)
        self.objects = objects or Manager(self)
        self._client = client
        self._model_name = model_name
        self._endpoint = endpoint
        self._schema = schema
        self._schema_data = self.client.schema.get()
        self._base_url = client._store["base_url"]
        self._fields = dict()

    def __repr__(self):
        return "<{0}: {1}>".format(self._model_name, self._endpoint)

    def __call__(self, **kwargs):


        return self

    def __setattr__(self, attr, value):
        super(Model, self).__setattr__(attr, value)
        self._set_field(attr, value)

    def _set_field(self, attr, value):
        if hasattr(self, "_schema_data"):
            if attr in self._schema_data["fields"]:
                field_type = self._schema_data["fields"][attr]["type"]
                check_type = False
                value_ = None
                try:
                    if field_type == "string":
                        check_type = isinstance(value, str)
                        value_ = value
                    elif field_type == "integer":
                        check_type = True  # "".isdigit(), isinstance(value, int)
                        value_ = value
                    elif field_type == "datetime":
                        check_type = True  # return isinstance(value, datetime)
                        value_ = value
                except Exception:
                    check_type = False
                finally:
                    if check_type is not True:
                        raise FieldTypeError(
                            "Field Type Error: '{0}' is '{1}' type. ( Input '{2}:{3}' )"
                                .format(attr, field_type, value_, type(value_).__name__))
                self._fields[attr] = value_

    def schema(self, *attrs):
        if attrs:
            s = self._schema_data
            for attr in attrs:
                s = s[attr]
            return s
        else:
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
