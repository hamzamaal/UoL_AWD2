"""WebSocket consumers for live chat functionality in the forum app."""

import json

from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    """Handle WebSocket connections for a simple room-based chat."""

    async def connect(self):
        """Join the requested room group and accept the socket connection."""
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        """Leave the room group when the socket disconnects."""
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        """Broadcast an incoming chat message to the current room group."""
        data = json.loads(text_data)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': data['message'],
                'username': data['username'],
            },
        )

    async def chat_message(self, event):
        """Send a broadcast message from the group back to the client."""
        await self.send(
            text_data=json.dumps(
                {
                    'message': event['message'],
                    'username': event['username'],
                }
            )
        )
