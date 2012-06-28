# -*- coding: utf-8 -*-
import slumber


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
        if True :
            return self._response[attr]
#            return #  Object
        elif related_type == "to_one":
            return #  Object
        elif related_type == "many":
            return #  Object
        elif related_type == "for":
            return #  Object

    def __getitem__(self, item):
        if item in self._response:
            return self._response[item]
        else:
            raise KeyError(item)

    def __contains__(self, attr):
        return attr in self._response


class QuerySet(object):

    def __init__(self, model, responses=None, **kwargs):
        self.model = model
        self._responses = responses
        self._objects = responses and dict(enumerate(responses["objects"]))
        self._meta = responses and responses["meta"]
        self._name = None  # self._name = name
        self._kwargs = kwargs
        self._response_class = kwargs.get("response_class", Response)

    def __repr__(self):
        return "<QuerySet {0} ({1}/{2})>".format(
                    self._response_class, len(self._objects), self.__len__())

    def __len__(self):
        return self._meta["total_count"]

    def __iter__(self):
        """ イテレータを拡張して続けてnextを呼ぶようにするのも面白いかも """
        return self._iter()

    def __getitem__(self, k):
        # TODO: slice, index
        NotImplementedError("# TODO: slice, index")

    def _iter(self):
        for i in self._objects:
            yield self._wrap_response(self._objects[i])

    def _wrap_response(self, dic):
        return self._response_class(self.model, dic)

    def get(self, *args, **kwargs):
        return

    def filter(self, *args, **kwargs):
        return self.__class__(self.model, self.model.client.get(*args, **kwargs))

#    def next(self):
#        """ request next page """
#        res = self._api.get(self._api.get_url(self._meta["next"]))
#        return PagerResponse(self._api, res)
#
#    def previous(self):
#        """ request previous page """
#        res = self._api.get(self._api.get_url(self._meta["previous"]))
#        return PagerResponse(self._api, res)


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
