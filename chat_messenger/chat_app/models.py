import uuid

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.utils import timezone
# User = settings.AUTH_USER


class Room(models.Model):
    name = models.CharField('Room Name', max_length=256, unique=True)
    description = models.TextField('Description', null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    uuid_id = models.UUIDField(default=uuid.uuid3, primary_key=True)
    time = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    text = models.TextField(max_length=1024)
    room = models.ForeignKey(Room, related_name="chat_messages", on_delete=models.CASCADE)
    seen = models.BooleanField(default=False)
    seen_time = models.DateTimeField(null=True, blank=True)
    delivered = models.BooleanField(default=False)

    def set_seen(self):
        if not self.seen:
            self.seen = True
            self.seen_time = timezone.now()
            self.save()

    def set_delivered(self):
        if not self.delivered:
            self.delivered = True
            self.save()

    class Meta:
        ordering = ['-time']
        get_latest_by = ['-time']
