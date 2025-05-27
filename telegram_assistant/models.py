import json
import datetime
from django.db import models
from django.utils import timezone

class Chat(models.Model):
    chat_id = models.BigIntegerField(unique=True)
    type = models.CharField(max_length=20)  # private, group, supergroup, channel
    title = models.CharField(max_length=255, null=True, blank=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    photo = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        if self.title:
            return f"{self.title} ({self.chat_id})"
        return f"{self.first_name or ''} {self.last_name or ''} ({self.chat_id})".strip()
    
    class Meta:
        ordering = ['-updated_at']

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    message_id = models.BigIntegerField()
    from_user_id = models.BigIntegerField(null=True, blank=True)
    from_user_name = models.CharField(max_length=255, null=True, blank=True)
    date = models.DateTimeField()
    text = models.TextField(null=True, blank=True)
    is_bot_message = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Message {self.message_id} in {self.chat}"
    
    class Meta:
        ordering = ['-date']
        unique_together = ('chat', 'message_id')