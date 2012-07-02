# -*- coding: utf-8 -*-
#from datetime import datetime
import copy
import urlparse
import slumber


__all__ = ["Client"]


class ObjectDoesNotExist(Exception):
    pass


class MultipleObjectsReturned(Exception):
    pass


class FieldTypeError(TypeError):
    pass


def parse_id(resouce_uri):
    return resouce_uri.split("/")[::-1][1]


class Response(object):

    def __init__(self, model, response=dict()):
        self.__dict__["_response"] = response
        self.model = model(**response)
        self._schema = self.model.schema()
        self._url = ""

    def _get_res(self):
        return self.__dict__["_response"]

    def _set_res(self, value):
        self.__dict__["_response"] = value

    def _get_response(self):
        return self._res

    def _set_response(self, value):
        self._res = value

    _res = property(_get_res, _set_res)
    _response = property(_get_response, _set_response)

    def __repr__(self):
        return "<{0}: {1} {2}>".format(self.model._model_name, self._url, self._res)

    def __getattr__(self, attr):
        if not attr in self._response:
            raise AttributeError(attr)
        elif not "related_type" in self._schema["fields"][attr]:
            return self._response[attr]

        related_type = self._schema["fields"][attr]["related_type"]
        if related_type == "to_many":
            return ManyToManyManager(model=self.model,
                            query={"id__in": [parse_id(url) for url in self._response[attr]]})
        elif related_type == "to_one":
            return LazyResponse(model=self.model, model_name=attr, url=self._response[attr])

    def __getitem__(self, item):
        if item in self._response:
            return self._response[item]
        else:
            raise KeyError(item)

    def __contains__(self, attr):
        return attr in self._res

    def __setattr__(self, attr, value):
        if self.__contains__(attr):
            self._res[attr] = value
            self.model.__setattr__(attr, value)
        super(Response, self).__setattr__(attr, value)

    def save(self):
        self.model.save()

    def delete(self):
        return


class LazyResponse(Response):
    """ convert response model and lazy response """

    def __init__(self, model_name, url, *args, **kwargs):
        super(LazyResponse, self).__init__(*args, **kwargs)
        self.model = self.model._clone(model_name)
        self._client = getattr(self.model._main_client, model_name)
        self._schema = self.model.schema()
        self._url = url

    def _get_response(self):
        if not self._res:
            self._res = self._client(parse_id(self._url)).get()
        return self._res

    def _set_response(self, value):
        self._res = value

    _response = property(_get_response, _set_response)


class QuerySet(object):

    def __init__(self, model, responses=None, **kwargs):
        self.model = model
        self._kwargs = kwargs
        self._result_cache = None
        self._responses = responses
        self._meta = responses["meta"] if responses else {"total_count": 0}
        self._objects = dict(enumerate(responses["objects"])) if responses else []
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
        k = klass(model=self.model, responses=responses)
        k.__dict__.update(kwargs)
        return k

    def _request(self, url):
        return self.model._base_client.request(url)

    def _next(self):
        """ request next page """
        if not self._meta["next"]:
            raise StopIteration()
        return self._clone(self._request(self._meta["next"]))

    def _previous(self):
        """ request previous page """
        if not self._meta["previous"]:
            raise StopIteration()
        return self._clone(self._request(self._meta["previous"]))

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
        return self._wrap_response(self.model._client(pk).get())

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

    def count(self):
        if self._objects:
            return self._meta["total_count"]
        return self.filter()._meta["total_count"]

    def all(self):
        return self.filter()

    def filter(self, *args, **kwargs):
        return self._filter(*args, **kwargs)

    def _filter(self, *args, **kwargs):

        # TODO: ↓↓↓ ManyToManyで 一件も relationがない場合の処理, 現状元のQuerySetの結果が返される ↓↓↓↓
        # <QuerySet <class 'queryset_client.client.Response'> (0/0)>

        kwargs_ = dict(self._query.items() + kwargs.items())
        clone = self._clone(self.model._client.get(**kwargs_))
        clone._query.update({
            "id__in": [parse_id(klass.resource_uri) for klass in clone[0:len(clone)]]
        })
        return clone

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

    def __init__(self, main_client, model_name, endpoint, schema, objects=None, base_client=None):
        self._client = getattr(main_client, model_name)
        self._main_client = main_client
        self._base_client = base_client
        self._model_name = model_name
        self._endpoint = endpoint
        self._schema = schema
        self._schema_store = self._base_client.schema(model_name)
        self._base_url = self._main_client._store["base_url"]
        self._fields = dict()  # TODO: set field attribute
        self._strict_field = True
        self.objects = objects or Manager(self)  # TODO: LazyCall

    def __repr__(self):
        return "<{0}: {1}{2}>".format(self._model_name, self._endpoint,
                                      " " + str(self._fields) if self._fields else "")

    def __call__(self, **kwargs):
        self._setattrs(**kwargs)  # TODO: LazyCall

        klass = copy.deepcopy(self)
        for field in self._fields:
            self.__delattr__(field)
        self._fields = dict()
        return klass

    def _clone(self, model_name, **kwargs):
        """ create `model_name` model """
        s = self._base_client.schema()[model_name]
        klass = self.__class__(self._main_client, model_name,
                               s["list_endpoint"], s["schema"], base_client=self._base_client)
        klass.__dict__.update(kwargs)
        return klass

    def _setattrs(self, **kwargs):
        for field in kwargs:
            self.__setattr__(field, kwargs[field])
            if not field in self._fields:
                raise FieldTypeError("'{0}' is an invalid keyword argument for this function"
                                     .format(field))

    def __setattr__(self, attr, value):
        self._setfield(attr, value)
        super(Model, self).__setattr__(attr, value)

    def _setfield(self, attr, value):
        if hasattr(self, "_schema_store"):
            if attr in self._schema_store["fields"]:
                nullable = self._schema_store["fields"][attr]["nullable"]
                blank = self._schema_store["fields"][attr]["blank"]
                field_type = self._schema_store["fields"][attr]["type"]

                check_type = False
                value_ = value
                try:
                    #  TODO: type check and convert value.
                    if nullable or blank:
                        check_type = True
#                        value_ = value
                    elif field_type == "string":
                        check_type = isinstance(value, (str, unicode))
#                        value_ = value
                    elif field_type == "integer":
                        check_type = True  # "".isdigit(), isinstance(value, int)
#                        value_ = value
                    elif field_type == "datetime":
                        check_type = True  # return isinstance(value, datetime)
#                        value_ = value
                    elif field_type == "related":
                        check_type = True  # return isinstance(value, datetime)
#                        value_ = value
                    elif field_type == "boolean":
                        check_type = True  # return isinstance(value, datetime)
#                        value_ = value
                except Exception:
                    check_type = False
                finally:
                    if check_type is not True and self._strict_field:
                        raise FieldTypeError(
                            "Field Type Error: '{0}' is '{1}' type. ( Input '{2}:{3}' )"
                                .format(attr, field_type, value_, type(value_).__name__))
                self._fields[attr] = value_  # set field

    def schema(self, *attrs):
        if attrs:
            s = self._schema_store
            for attr in attrs:
                s = s[attr]
            return s
        else:
            return self._schema_store

    def save(self):
        if hasattr(self, "id"):
            self._client(self.id).put(self._fields)  # return bool
        else:
            self._setattrs(**self._client.post(self._fields))

    def delete(self):
#        self._client.delete()
        pass


class SchemaStore(dict):
    """ schema cache """

    def __setattr__(self, name, value):
        self[name] = value

    def __getattr__(self, name):
        return self[name]

    def quick_get(self, name, schema):
        if not self.__contains__(name):
            self.__setattr__(name, schema())
        return self[name]


class SchemaMeta(type):

    def __new__(cls, name, bases, attrs):
        new_class = super(SchemaMeta, cls).__new__(cls, name, bases, attrs)
        new_class._schema_store = getattr(new_class, "_schema_store", SchemaStore())
        return new_class


class Client(object):

    __metaclass__ = SchemaMeta

    def __init__(self, base_url, auth=None, client=None):
        self._main_client = (client or slumber.API)(base_url, auth)
        self._base_url = self._main_client._store["base_url"]
        self._method_gen()

    def request(self, url, method="GET"):
        request_url = self._url_gen(url)
        s = self._main_client._store
        requests = s["session"]
        serializer = slumber.serialize.Serializer(default_format=s["format"])
        return serializer.loads(requests.request(method, request_url).content)

    def schema(self, model_name=None):
        if not model_name in self._schema_store:
            request_url = self._url_gen("{0}/schema/".format(model_name)) if \
                                                              model_name else self._base_url
            self._schema_store[model_name] = self.request(request_url)
        return self._schema_store[model_name]

    def _url_gen(self, url):
        parse = urlparse.urlparse(url)
        if not parse.scheme:
            url_ = urlparse.urljoin(self._base_url, parse.path)
            if parse.query:
                return urlparse.urljoin(url_, "?{0}".format(parse.query))
            return url_
        else:
            return url

    def _method_gen(self, base_client=None):
        base_client = base_client or copy.deepcopy(self)
        s = self.schema()
        for model_name in s:
            setattr(self, model_name, Model(self._main_client, model_name,
                    s[model_name]["list_endpoint"], s[model_name]["schema"],
                    base_client=base_client))
