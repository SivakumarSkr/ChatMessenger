from channels.generic.websocket import AsyncJsonWebsocketConsumer


class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        user = self.scope['user']
        if user.is_anonymous:
            await self.close()
        else:
            await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive_json(self, content, **kwargs):
        command = content.get('command', None)
        if command == 'join':
            await self.join_room(content['room'])
        elif command == 'send':
            await self.send_json(content['room'], content['message'])
        elif command == 'leave':
            await self.leave_room(content['room'])

    async def join_room(self, room_id):
        await self.channel_layer.group_send(
            room_id,
            {
                'type': 'chat.join',
                'room_id': room_id,
                'username': self.scope['user'].username
            }
        )
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_layer
        )
        await self.send_json(
            {
                'join': str(room_id)
            }
        )

    async def leave_room(self, room_id):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat.leave',
                'room_id': room_id,
                'username': self.scope['user'].username
            }
        )
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        await self.send_json(
            {
                'leave': str(self.room_name)
            }
        )

    async def send_room(self, room_id, message):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat.message',
                'room_id': room_id,
                'username': self.scope['user'].username,
                'message': message
            }
        )

    async def chat_message(self, event):
        message = event['message']
        await self.send_json({
            'message': message,
            'username': event['username'],
            'room': event['room_id']
        })

    async def chat_join(self, event):
        await self.send_json(
            {
                'room': event['room_id'],
                'username': event['username']
            }
        )

    async def chat_leave(self, event):
        await self.send_json(
            {
                'room': event['room_id'],
                'username': event['username'],
            }
        )
