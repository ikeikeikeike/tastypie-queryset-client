import string
import random


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))


class FixtureMixin(object):

    def setUp(self):
        super(FixtureMixin, self).setUp()
        for i in xrange(0, 12):
            message = self.client.message()
            message.subject = id_generator()
            message.body = id_generator()
            message.save()

            inbox = self.client.inbox()
            inbox.did = id_generator()
            inbox.save()

            inbox_message = self.client.inbox_message()
            inbox_message.message = message.resource_uri
            inbox_message.inbox = inbox.resource_uri
            inbox_message.save()

#            inbox_message_many = self.client.inbox_message_many()
#            inbox_message_many.inbox_message = inbox_message.resource_uri
#            inbox_message_many.save()