from django.contrib import admin

from chat.models import Chat, ChatMessage, UserOnlineStatus

admin.site.register(Chat)
admin.site.register(ChatMessage)
admin.site.register(UserOnlineStatus)
