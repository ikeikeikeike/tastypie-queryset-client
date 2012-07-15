from django.db import (
    models,
    transaction
)
from django.utils.translation import ugettext


class Inbox(models.Model):
    """ Inbox """
    did = models.CharField(ugettext("device id"), max_length="250")
    ctime = models.DateTimeField(ugettext("ctime"), auto_now_add=True)
    utime = models.DateTimeField(ugettext("utime"), auto_now=True)

    class Meta:
        verbose_name = ugettext("inbox")
        verbose_name_plural = ugettext("inboxes")

    def __unicode__(self):
        return u"{0}".format(self.did)


class Message(models.Model):
    """ Messages """
    subject = models.CharField(ugettext("subject"), max_length="250")
    body = models.TextField(ugettext("body"))
    ctime = models.DateTimeField(ugettext("ctime"), auto_now_add=True)
    utime = models.DateTimeField(ugettext("utime"), auto_now=True)

    class Meta:
        verbose_name = ugettext("message")
        verbose_name_plural = ugettext("messages")

    def __unicode__(self):
        return u"{0}".format(self.subject)


class InboxMessage(models.Model):
    """ InboxMessage """
    inbox = models.ForeignKey(Inbox, unique=False, db_index=True, help_text=ugettext("inbox == mailto"))
    message = models.ForeignKey(Message, unique=False, db_index=True, null=True)
    mailfrom = models.CharField(ugettext("mailfrom"), max_length="250", blank=True, null=True, help_text=ugettext("Anyway"))
    read = models.NullBooleanField(ugettext("read"), db_index=True, help_text=ugettext("null=new, 0=unread, 1=read"))
    ctime = models.DateTimeField(ugettext("ctime"), auto_now_add=True)
    utime = models.DateTimeField(ugettext("utime"), auto_now=True)

    class Meta:
        verbose_name = ugettext("inbox_message")
        verbose_name_plural = ugettext("inbox_messages")
        unique_together = (("inbox", "message"))  # multi unique key

    def __unicode__(self):
        return u"{0} ({1})".format(self.inbox, self.message)


class InboxMessageMany(models.Model):
    """ InboxMessage Many """
    inbox_message = models.ManyToManyField(InboxMessage, null=True)
    ctime = models.DateTimeField(ugettext("ctime"), auto_now_add=True)
    utime = models.DateTimeField(ugettext("utime"), auto_now=True)


class Operation(models.Model):
    """  """
    opid = models.CharField(ugettext("opid"), max_length="250", help_text=ugettext("operation id (UUID)"))
    name = models.CharField(ugettext("name"), max_length="250", help_text=ugettext("operation type name"))
    meta = models.TextField(ugettext("meta"), help_text=ugettext("operation meta data."))
    ctime = models.DateTimeField(ugettext("ctime"), auto_now_add=True)
    utime = models.DateTimeField(ugettext("utime"), auto_now=True)

    class Meta:
        verbose_name = ugettext("operation")
        verbose_name_plural = ugettext("operations")

    def __unicode__(self):
        return u"name: {0}, opid: {1}".format(self.name, self.opid)


class Status(models.Model):

    operation = models.ForeignKey(Operation, unique=False, db_index=True)
    contenttype = models.ForeignKey(InboxMessage, unique=False, db_index=True,
                                    help_text=ugettext("# TODO: fix contenttype framework"))
    status = models.CharField(ugettext("status"), db_index=True, max_length="20", default="ready")
    reason = models.CharField(ugettext("reason"), max_length="250", blank=True)
    trace = models.TextField(ugettext("stack trace"), blank=True)
    ctime = models.DateTimeField(ugettext("ctime"), auto_now_add=True)
    utime = models.DateTimeField(ugettext("utime"), auto_now=True)

    class Meta:
        verbose_name = ugettext("status")
        verbose_name_plural = ugettext("statuses")
        unique_together = (("operation", "contenttype"))  # multi unique key

    def __unicode__(self):
        return u"operation: {0}, contenttype: {1}, status: {2}".format(self.operation, self.contenttype, self.status)