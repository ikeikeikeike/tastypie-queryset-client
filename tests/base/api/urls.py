from django.conf.urls.defaults import (
    patterns,
    include
)
from tastypie.api import Api
from .resources import *

api = Api(api_name="v1")
api.register(InboxResource())
api.register(MessageResource())
api.register(InboxMessageResource())
api.register(InboxMessageManyResource())

urlpatterns = patterns('',
    (r'^base/', include(api.urls)),
)
