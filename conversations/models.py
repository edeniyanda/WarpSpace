from django.db import models
from django.contrib.auth.models import User

class Chat(models.Model):
    users = models.ManyToManyField(User, related_name='chats')
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-modified_at']

class ConversationMessage(models.Model):
    conversation = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)

    class Meta:
        ordering = ['created_at']

    def save(self, *args, **kwargs):
        self.conversation.save()

        super(ConversationMessage, self).save(*args, **kwargs)