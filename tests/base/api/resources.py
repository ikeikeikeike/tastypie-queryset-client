# external library
from tastypie import fields
from tastypie.resources import (
    # Resource,
    ModelResource,
    ALL,
    ALL_WITH_RELATIONS
)
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

