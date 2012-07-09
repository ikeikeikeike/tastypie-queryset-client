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