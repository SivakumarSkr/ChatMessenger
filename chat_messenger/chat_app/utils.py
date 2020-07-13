from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser

from chat_app.models import Message, Room


@database_sync_to_async
def create_message(**message):
    if not message.get('user', AnonymousUser()).user.is_authenticated:
        raise Exception('User is not authenticated')

    try:
        message_obj = Message.objects.create(message)
    except Exception as e:
        raise Exception('Failed to create message.')
    else:
        return message_obj


@database_sync_to_async
def get_room(room_name):
    try:
        room = Room.objects.get(name=room_name)
    except Exception as e:
        raise Exception('Failed to get room.')
    else:
        return room
