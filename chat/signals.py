# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import UserOnlineStatus
# import json

# from channels.layers import get_channel_layer
# from asgiref.sync import async_to_sync


# @receiver(post_save, sender=UserOnlineStatus)
# def send_online_status(sender, instance, created, **kwargs):
#     if not created:
#         channel_layer = get_channel_layer()
#         user = instance.user.id
#         user_status = instance.online_status

#         data = {
#             'user_id': user,
#             'status': user_status
#         }
#         async_to_sync(channel_layer.group_send)( #type: ignore
#             'online_users', {
#                 'type':'user_status',
#                 'value':json.dumps(data)
#             }
#         )