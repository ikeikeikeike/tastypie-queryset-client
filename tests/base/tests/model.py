from testcases import (
    TestServerTestCase,
    get_client
)
from queryset_client.client import (
    FieldTypeError,
    ObjectDoesNotExist
)
from .utils import id_generator


class ModelTestCase(TestServerTestCase):

    def setUp(self):
        self.start_test_server()
        self.client = get_client()

    def tearDown(self):
        self.stop_test_server()
    
    def test_type1(self):
        value = 1
        self.client.message.id = value
        self.assertTrue(self.client.message.id == value)
        self.assertTrue(self.client.message._fields["id"] == value)
    
    def test_type2(self):
        value = 1
        try:
            self.client.message.subject = value
        except FieldTypeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)
        
    def test_call1(self):
        subject = "subject call 1"
        body = "body call 1"
        message_obj = self.client.message(subject=subject, body=body)
        self.assertTrue(message_obj.subject == subject)
        self.assertTrue(message_obj.body == body)
        
    def test_call2(self):
        try:
            self.client.message(errorfield="oha yo! oha yo!")
        except FieldTypeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)
        
    def test_save1(self):
        """ (new) """
        subject = "subject save 1"
        body = "body save 1"
        message = self.client.message(subject=subject, body=body)
        message.save()
    
        message_ = self.client.message.objects.get(id=message.id, subject=subject, body=body)
        self.assertTrue(message_.id == message.id)
        self.assertTrue(message_.subject == message.subject)
        self.assertTrue(message_.body == message.body)
        
    def test_save2(self):
        """ (update) """
        subject1 = "subject save 2"
        body1 = "body save 2"
        message = self.client.message(subject=subject1, body=body1)
        message.save()
    
        subject2 = "subject save 2 update"
        body2 = "body save 2 update"
        message.subject = subject2
        message.body = body2
        message.save()
        try:
            self.client.message.objects.get(id=message.id, subject=subject1, body=body1)
        except ObjectDoesNotExist:
            self.assertTrue(True)
        else:
            self.assertTrue(False)
    
        try:
            message_ = self.client.message.objects.get(id=message.id, subject=subject2, body=body2)
        except ObjectDoesNotExist:
            self.assertTrue(False)
        else:
            self.assertTrue(True)
            self.assertTrue(message_.id == message.id)
            self.assertTrue(message_.subject == message.subject)
            self.assertTrue(message_.body == message.body)
        
    def test_save3(self):
        """ (update) for query_set """
    
        subject = id_generator()
        body = id_generator()
    
        for message in self.client.message.objects.filter(id__in=xrange(20, 33)):
            message.subject = subject
            message.body = body
            message.save()
    
        for message in self.client.message.objects.filter(id__in=xrange(20, 33)):
            self.assertTrue(message.subject == subject)
            self.assertTrue(message.body == body)
        
    def test_save_rel1(self):
        """ relation """
    #    subject = ""
    #    body = ""
    #    message = self.client.inbox_message(subject=subject, body=body)
    #    message.save()
        
    def test_save_many1(self):
        """ many to many """
    #    subject = ""
    #    body = ""
    #    message = self.client.inbox_message_many(inbox_message=inbox_message)
    #    message.save()
        
    def test_delete1(self):
        subject = "subject delete 1"
        body = "body delete 1"
        message = self.client.message(subject=subject, body=body)
        message.save()
    
        message_ = self.client.message.objects.get(id=message.id, subject=subject, body=body)
        self.assertTrue(message_.id == message.id)
        self.assertTrue(message_.subject == message.subject)
        self.assertTrue(message_.body == message.body)
    
        message.delete()
        try:
            message.id
        except AttributeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)
    
        try:
            message_.delete()
        except Exception:
            self.assertTrue(True)
        else:
            self.assertTrue(False)
        try:
            message.id
        except AttributeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)
