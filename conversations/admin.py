from django.contrib import admin
from .models import Chat, ConversationMessage

admin.site.register([Chat, ConversationMessage])

