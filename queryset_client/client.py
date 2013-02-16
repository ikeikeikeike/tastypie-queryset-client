# -*- coding: utf-8 -*-
from datetime import datetime
import copy
import decimal
import slumber
import urlparse


__all__ = ["Client"]


class ObjectDoesNotExist(Exception):
    pass


class MultipleObjectsReturned(Exception):
    pass


class FieldTypeError(TypeError):
    pass


class QuerySet(object):

    def __init__(self, model, responses=None, query=None, **kwargs):
        self.model = model
        self._kwargs = kwargs
        self._query = query or dict()
        self._iteration_num = None
        self._response_class = kwargs.get("response_class", Response)
        self._set_objects(responses)  # set _responses, _meta, _objects, _objects_count

    def __repr__(self):
        if self.__objects is None:
            numerator = 0
        else:
            numerator = len(self._objects)
        return "<QuerySet {0} ({1}/{2})>".format(
                    self._response_class, numerator, len(self))

    def __len__(self):
        """ total count """
        if self._iteration_num is None:
            return self.count()
        return self._iteration_num

    def __iter__(self):
        if len(self._objects) < 1\
        or len(self._objects) < len(self):
            return self._iteration()
        return iter(self._objects)

    def _iteration(self):
        if len(self) < 1:
            raise StopIteration()
        index, length = 0, 0
        klass = self._clone(self._responses)  # klass = copy.deepcopy(self)
        while 1:
            try:
                yield klass._objects[index]
                index += 1
                length += 1
            except IndexError:
                if self._iteration_num <= length \
                and self._iteration_num is not None:
                    raise StopIteration()
                klass = klass._next()
                self._objects.extend(klass._objects)
                index = 0

    def __get_objects(self):
        if self.__objects is not None \
        and isinstance(self.__objects, (tuple, list)):
            for i, obj in enumerate(self.__objects):
                if isinstance(obj, dict) is True:
                    self.__objects[i] = self._wrap_response(obj)
            return self.__objects
        else:
            return []

    def __set_objects(self, value):
        self.__objects = value

    _objects = property(__get_objects, __set_objects)

    def _fill_objects(self):
        self._set_objects(self._get_responses())

    def _set_objects(self, responses):
        self._responses = responses
        self._meta = responses and responses["meta"]
        self._objects = responses and responses["objects"]

    def _clone(self, responses=None, klass=None, **kwargs):
        responses = responses or self._responses
        klass = klass or self.__class__

        clone = klass(model=self.model, responses=responses, query=self._query)
        clone.__dict__.update(kwargs)
        return clone

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
                # step = index.step
                start = index.start or 0
                stop = index.stop
                limit = stop - start

                self._iteration_num = limit
                query = dict(self._query.items() + {"limit": limit, "offset": start}.items())
                responses = self._get_responses(**query)

                clone = self._clone(responses, _iteration_num=self._iteration_num)
                clone._query.update({"id__in": clone._get_ids()})
                return clone

            if not self._responses:
                self._fill_objects()
            return self._objects[index]
        except KeyError as err:
            raise IndexError(err)

    def _get_responses(self, **kwargs):
        return self.model._client.get(**kwargs)

    def _wrap_response(self, dic):
        return self._response_class(self.model, dic)

    def get_pk(self, pk):
        return self._wrap_response(self.model._client(pk).get())

    def count(self):
        if self._responses:
            return self._meta["total_count"]
        self._fill_objects()
        return self._meta["total_count"]

    def get(self, *args, **kwargs):
        """ create

        :param args: XXX no descript
        :param kwargs: XXX no descript
        :rtype: Response
        :return: Response object.
        """
        clone = self.filter(*args, **kwargs)
        num = len(clone._objects)
        if num > 1:
            raise MultipleObjectsReturned(
                "get() returned more than one {0} -- it returned {1}! Lookup parameters were {2}"
                    .format(self.model._model_name, num, kwargs))
        elif not num:
            raise ObjectDoesNotExist("{0} matching query does not exist."
                    .format(self.model._model_name))
        return clone[0]

    def create(self, **kwargs):
        """ create

        :param kwargs: XXX No Description
        :rtype: Model
        :return: created object.
        """
        obj = self.model(**kwargs)
        obj.save()
        return obj

    def get_or_create(self, **kwargs):
        """

        :param kwargs: field
        :rtype: tuple
        :return: Returns a tuple of (object, created)
        """
        assert kwargs, 'get_or_create() must be passed at least one keyword argument'

        try:
            return self.get(**kwargs), False
        except ObjectDoesNotExist:
            obj = self.model(**kwargs)
            obj.save()
            return obj, True

    def latest(self, field_name=None):
        assert bool(field_name), \
            "latest() requires either a field_name parameter or 'get_latest_by' in the model"
        clone = self._filter(**{"order_by": "-{0}".format(field_name), "limit": 1})
        return clone[0]

    def exists(self):
        if not self._responses:
            self._fill_objects()
        return bool(self._objects)

    def all(self):
        return self._clone()

    def filter(self, *args, **kwargs):
        return self._filter(*args, **kwargs)

    def _get_ids(self):
        return [parse_id(obj["resource_uri"]) for obj in self._objects]

    def _filter(self, *args, **kwargs):
        """

        .. note:: No request args(== Empty request params).

            -  * e.g. id__in=[] -> http://no.com/?any=search
            -  o e.g. id__in=[] -> http://no.com/?any=search&id__in=

        .. note:: Overwrite id__in

        """

        # TODO: Bugs? in the requests package. (The Issue #??).
        query = dict(self._query.items() + kwargs.items())
        clone = self._clone(self._get_responses(**query))
        clone._query.update({"id__in": clone._get_ids()})
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
        return self.get_query_set()

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

    def get_or_create(self, **kwargs):
        return self.get_query_set().get_or_create(**kwargs)

    def create(self, **kwargs):
        return self.get_query_set().create(**kwargs)

#    TODO: next implementation
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

    def latest(self, *args, **kwargs):
        return self.get_query_set().latest(*args, **kwargs)

    def order_by(self, *args, **kwargs):
        return self.get_query_set().order_by(*args, **kwargs)

#    def select_for_update(self, *args, **kwargs):
#        return self.get_query_set().select_for_update(*args, **kwargs)

#    def select_related(self, *args, **kwargs):
#        return self.get_query_set().select_related(*args, **kwargs)

#    def prefetch_related(self, *args, **kwargs):
#        return self.get_query_set().prefetch_related(*args, **kwargs)

#    def values(self, *args, **kwargs):
#        return self.get_query_set().values(*args, **kwargs)

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

    def exists(self, *args, **kwargs):
        return self.get_query_set().exists(*args, **kwargs)


class ManyToManyManager(Manager):

    def __init__(self, query=None, instance=None, **kwargs):
        super(ManyToManyManager, self).__init__(**kwargs)
        self._query = query or dict()
        self._instance = instance

    def get_query_set(self):
        return QuerySet(self.model, query=self._query).filter()

    def filter(self, *args, **kwargs):
        if "id__in" in kwargs:
            raise NotImplementedError("'id__in' does not allowed in ManyToManyManager.")
        return QuerySet(self.model, query=self._query).filter(*args, **kwargs)

    def add(self, *objs):
        """

        .. note::
            After executing a add method, does not execute saving. You must be manual operation to the save method.

        .. todo::
            signal save

        """
        if objs:
            resource_models = getattr(self._instance, self.model._model_name)
            query_ids = self._query.get("id__in", [])
            for obj in objs:
                resource_uri = getattr(obj, "resource_uri")

                resource_models.append(resource_uri)
                query_ids.append(parse_id(resource_uri))
            self._query.update({"id__in": list(set(query_ids))})
            setattr(self._instance, self.model._model_name, list(set(resource_models)))

    def remove(self, *objs):
        """

        .. note::
            After executing a add method, does not execute saving. You must be manual operation to the save method.

        .. todo::
            signal save

        """
        if objs:
            resource_models = getattr(self._instance, self.model._model_name)
            query_ids = self._query.get("id__in", [])
            for obj in objs:
                resource_uri = getattr(obj, "resource_uri")

                resource_models.remove(resource_uri)
                query_ids.remove(parse_id(resource_uri))
            self._query.update({"id__in": list(set(query_ids))})
            setattr(self._instance, self.model._model_name, list(set(resource_models)))

    def clear(self):
        """

        .. note::
            After executing a add method, does not execute saving. You must be manual operation to the save method.

        .. todo::
            signal save

        """
        self._query.update({"id__in": list()})
        setattr(self._instance, self.model._model_name, list())


def parse_id(resource_uri):
    """ url parsing

    :param resource_uri:
    :rtype: str
    :return: Primary id
    """
    return resource_uri.split("/")[::-1][1]


class Response(object):
    """ Proxy Model Class """
    def __init__(self, model, response=None, url=None, **kwargs):
        """
        :param model: The Model.
        :param response: Response from client library.
        """
        self.__response = response or dict()
        self._schema = model.schema()
        self._to_many_class = kwargs.get("_to_many_class", ManyToManyManager)
        self._to_one_class = kwargs.get("_to_one_class", self.__class__)
        self._url = url
        if url is None:
            self.model = model(**self.__response)
        else:
            self.model = model

    def __repr__(self):
        return "<{0}: {1} {2}>".format(
            self.model._model_name, self._url or "", self.__response)

    def __getattr__(self, attr):
        """ return Response Class """
        if not attr in self._response:
            raise AttributeError(attr)
        elif not "related_type" in self._schema["fields"][attr]:
            return self.__getitem__(attr)

        related_type = self._schema["fields"][attr]["related_type"]
        model = self.model.clone(attr)
        url = self._response[attr]
        if related_type == "to_many":
            return self._to_many_class(model=model,
                   query={"id__in": [parse_id(u) for u in url]}, instance=self.model)
        elif related_type == "to_one":
            return self._to_one_class(model=model, url=url)

    def __getitem__(self, item):
        if item in self._response:
            return getattr(self.model, item)
        else:
            raise KeyError(item)

    def __contains__(self, attr):
        if hasattr(self, "_response") is False:
            return False
        return attr in self._response

    def __setattr__(self, attr, value):
        if "model" in self.__dict__:
            if hasattr(self, attr):
                self.__response[attr] = value
                setattr(self.model, attr, value)
        super(Response, self).__setattr__(attr, value)

    @property
    def _response(self):
        if "model" in self.__dict__:
            if not self.__response:
                client = getattr(self.model._main_client, self.model._model_name)
                self.__response = client(parse_id(self._url)).get()
                self.model = self.model(**self.__response)
        return self.__response

    def save(self):
        """ save saved response """
        self.model.save()
        self.__response = self.model._get_fields()

    def delete(self):
        """ remove saved response """
        self.model.delete()
        self.__response = dict()


def model_gen(**configs):
    """ generate model

    :param slumber main_client:
    :param str model_name: resource name
    :param str endpoint: endpoint url
    :param str schema: schema url
    :param bool strict_field: strict field and convert value in field. ( default: True )
    :param Manager objects: Manager Class
    :param Client objects: Client Class
    """
    class Model(object):
        """ Inner Class
        """
        _client = getattr(configs.get("main_client"), configs.get("model_name"))
        _main_client = configs.get("main_client")
        _base_client = configs.get("base_client")
        _model_name = configs.get("model_name")
        _endpoint = configs.get("endpoint")
        _schema = configs.get("schema")
        _strict_field = configs.get("strict_field", True)
        _schema_store = _base_client.schema(_model_name)
        _base_url = _main_client._store["base_url"]
        _fields = dict()  # TODO: set field attribute
        objects = None

        def __init__(self, **kwargs):
            self._clear_fields()
            self._setattrs(**kwargs)  # TODO: LazyCall

        def __repr__(self):
            return "<{0}: {1}{2}>".format(self._model_name, self._endpoint,
                                          " " + str(self._fields) if self._fields else "")

        def _clear_fields(self, klass=None):
            c = klass or self
            for field in c._fields:
                c.__delattr__(field)
            c._fields = dict()

        def _setattrs(self, **kwargs):
            for field in kwargs:
                self.__setattr__(field, kwargs[field])
                if not field in self._fields:
                    raise FieldTypeError("'{0}' is an invalid keyword argument for this function"
                                         .format(field))

        def __setattr__(self, attr, value):
            self._setfield(attr, value)

        def _setfield(self, attr, value):
            if hasattr(self, "_schema_store"):
                if attr in self._schema_store["fields"]:
                    nullable = self._schema_store["fields"][attr]["nullable"]
                    blank = self._schema_store["fields"][attr]["blank"]
                    field_type = self._schema_store["fields"][attr]["type"]
                    check_type = False
                    err = ""
                    if self._strict_field is True:
                        try:
                            if (nullable or blank) and not value:
                                check_type = True
                            elif field_type == "string":
                                check_type = isinstance(value, (str, unicode))
                            elif field_type == "integer":
                                if isinstance(value, (str, unicode)):
                                    check_type = value.isdigit()
                                elif isinstance(value, int):
                                    check_type = True
                            elif field_type == "float":
                                if isinstance(value, float):
                                    check_type = True
                            elif field_type == "decimal":
                                value = decimal.Decimal(value)
                                check_type = isinstance(value, decimal.Decimal)
                            elif field_type == "datetime":
                                if isinstance(value, (str, unicode)):
                                    try:
                                        value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                                    except ValueError:
                                        value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")
                                check_type = isinstance(value, datetime)
                            elif field_type == "time":
                                check_type = True
                            elif field_type == "boolean":
                                check_type = True
                            if field_type == "related":
                                check_type = True
                        except Exception, err:
                            check_type = False
                        finally:
                            if check_type is not True:
                                raise FieldTypeError(
                                    "'{0}' is '{1}' type. ( Input '{2}:{3}' ) {4}"
                                        .format(attr, field_type, value, type(value).__name__, err))
                    self._fields[attr] = value  # set field
            super(Model, self).__setattr__(attr, value)

        def _get_field(self, field):
            if field in self._schema_store["fields"]:
                field_type = self._schema_store["fields"][field]["type"]
                value = self._fields[field]
                if self._strict_field is True:
                    try:
                        if field_type == "string":
                            pass
                        elif field_type == "integer":
                            pass   # input safe
                        elif field_type == "float":
                            pass   # input safe
                        elif field_type == "decimal":
                            pass   # input safe
                        elif field_type == "datetime":
                            value = value.isoformat()
                        elif field_type == "time":
                            pass
                        elif field_type == "boolean":
                            pass
                        else:
                            pass
                    except Exception:
                        if self._strict_field is True:
                            raise FieldTypeError(
                                "'{0}' is '{1}' type. ( Input '{2}:{3}' )"
                                    .format(field, field_type, value, type(value).__name__))
                if field_type == "related":
                    value = getattr(value, "resource_uri", value)
                    if self._schema_store["fields"][field]["related_type"] == "to_many":
                        if isinstance(value, (list, tuple)) is False:
                            value = [value]
                return value

        def _get_fields(self):
            fields = {}
            for field in self._fields:
                fields.update({field: self._get_field(field)})
            return fields

        @classmethod
        def clone(cls, model_name=None):
            """ create `model_name` model """
            return cls._base_client._model_gen(model_name or cls._model_name)

        @classmethod
        def schema(cls, *attrs):
            """

            * attrs example ::

                    >>> self.schema("fields")
                    # out fields schema
                    >>> self.schema("fields", "id")
                    # out id schema

            :param tuple attrs:
            :rtype: dict
            :return: model schema
            """
            if attrs:
                s = cls._schema_store
                for attr in attrs:
                    s = s[attr]
                return s
            else:
                return cls._schema_store

        def save(self):
            """ save

            :rtype: NoneType
            """
            if hasattr(self, "id"):
                self._client(self.id).put(self._get_fields())  # return bool
            else:
                self._client.post(self._get_fields())
                self._setattrs(**self._client._handle_redirect(self._client._))

        def delete(self):
            """ delete

            :rtype: NoneType
            """
            assert hasattr(self, "id") is True, "{0} object can't be deleted because its {2} attribute \
                is set to None.".format(self._model_name, self._schema_store["fields"]["id"]["type"])
            self._client(self.id).delete()
            self._clear_fields()

    Model.objects = configs.get("objects", Manager(Model))
    return Model


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


class ClientMeta(type):

    def __new__(cls, name, bases, attrs):
        klass = super(ClientMeta, cls).__new__(cls, name, bases, attrs)
        klass._schema_store = getattr(klass, "_schema_store", SchemaStore())
        return klass


class Client(object):

    __metaclass__ = ClientMeta

    def __init__(self, base_url, auth=None, strict_field=True, client=None):
        """

        :param str base_url: e.g. http://api.base.biz/base/v1/
        :param auth:
        :param bool strict_field: strict field and convert value in field.
        :param object client:
        """
        self._main_client = (client or slumber.API)(base_url, auth)
        self._base_url = self._main_client._store["base_url"]
        self._methods_gen(strict_field)

    def request(self, url, method="GET"):
        """ base requester

        * accept format below for **url**.

          1. http://api.base.biz/base/v1/path/to/api/?id=1
          #. /base/v1/path/to/api/?id=1
          #. /v1/path/to/api/?id=1
          #. /path/to/api/?id=1

        :param str url: target url
        :param str method: GET or POST (default: GET)
        :rtype: json
        :return: json object
        """
        request_url = self._url_gen(url)
        s = self._main_client._store
        requests = s["session"]
        serializer = slumber.serialize.Serializer(default=s["format"])
        return serializer.loads(requests.request(method, request_url).content)

    def schema(self, model_name=None):
        """ receive schema

        :param str model_name: resource class name
        :rtype: dict
        :return: schema dictionary
        """
        if not model_name in self._schema_store:
            url = self._url_gen("{0}/schema/".format(model_name)) if model_name \
                                                                 else self._base_url
            self._schema_store[model_name] = self.request(url)
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

    def _methods_gen(self, strict_field=True):
        for model_name in self.schema():
            setattr(self, model_name, self._model_gen(model_name, strict_field))

    def _model_gen(self, model_name, strict_field=True, base_client=None):
        schema = self.schema()
        return model_gen(
            main_client=self._main_client, model_name=model_name,
            endpoint=schema[model_name]["list_endpoint"], schema=schema[model_name]["schema"],
            strict_field=strict_field, base_client=base_client or copy.copy(self))
