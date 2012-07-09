from tastypie.authorization import Authorization                                                                                                                                    
from tastypie.authentication import Authentication

class ThroughAuthentication(Authentication):

    def is_authenticated(self, request, **kwargs):
        return True

    def get_identifier(self, request):
        return 1


class ThroughAuthorization(Authorization):

    def is_authorized(self, request, object=None):
        return True