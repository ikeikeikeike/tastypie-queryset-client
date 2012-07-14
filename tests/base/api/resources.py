# external library
from django.conf.urls import url
from django.core.paginator import Paginator
from tastypie import fields
from tastypie.resources import (
    # Resource,
    ModelResource,
    ALL,
    ALL_WITH_RELATIONS
)
from tastypie.utils.urls import trailing_slash
from .auth import (
    ThroughAuthentication,
    ThroughAuthorization
)

# applications
from .. import models as mdl


class InboxResource(ModelResource):
    """ Inbox Model Resource """

    class Meta:
        queryset = mdl.Inbox.objects.all()
        resource_name = 'inbox'
        filtering = {
            # allow attributes
            "id": ALL,
            "did": ALL
        }
        authentication = ThroughAuthentication()
        authorization = ThroughAuthorization()


class MessageResource(ModelResource):
    """ Message Model Resource """

    class Meta:
        queryset = mdl.Message.objects.all()
        resource_name = 'message'
        filtering = {
            # allow attributes
            "id": ALL,
            "subject": ALL,
            "body": ALL
        }
        ordering = (
            "id",
            "body",
        )
        authentication = ThroughAuthentication()
        authorization = ThroughAuthorization()


    def prepend_urls(self):
        """ dispatcher """
        return [
            url(r"^(?P<resource_name>{0})/paginator{1}$".format(
                self._meta.resource_name, trailing_slash()),
                self.wrap_view('paginator'), name="apimethod-message-paginator"),
        ]

    def paginator(self, request, **kwargs):
        """  """
        message = mdl.Message.objects.all()

#        mes = message[0:100]
#        print type(mes)
#
#        try:
#            for i in message:
#                print i
#        except Exception:
#            pass
#
#        try:
#            print message.count()
#        except Exception:
#            pass

        p = Paginator(message, 100)

        page = p.page(3)
        try:
            num = 0
            for num, i in page:
                pass
        except Exception:
            pass

        page = p.page(1)
        try:
            num = 0
            for num, i in enumerate(page):
                pass
        except Exception:
            pass

        return {}


class InboxMessageResource(ModelResource):
    """ Inbox Model Resource """

    inbox = fields.ForeignKey(InboxResource, "inbox")
    message = fields.ForeignKey(MessageResource, "message")

    class Meta:
        resource_name = 'inbox_message'
        queryset = mdl.InboxMessage.objects.all()
        filtering = {
            # allow attributes
            "id": ALL,
            "inbox": ALL_WITH_RELATIONS,
            "message": ALL_WITH_RELATIONS
        }
        authentication = ThroughAuthentication()
        authorization = ThroughAuthorization()



class InboxMessageManyResource(ModelResource):
    """  """

    inbox_message = fields.ManyToManyField(InboxMessageResource, "inbox_message")

    class Meta:
        resource_name = "inbox_message_many"
        queryset = mdl.InboxMessageMany.objects.all()
        filtering = {
            # allow attributes
            "id": ALL,
            "inbox_message": ALL_WITH_RELATIONS,
        }
        authentication = ThroughAuthentication()
        authorization = ThroughAuthorization()

