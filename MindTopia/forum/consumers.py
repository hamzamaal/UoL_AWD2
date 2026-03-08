"""WebSocket consumers for forum real-time chat."""

import json

from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser

from .models import ChatMessage


class ChatConsumer(AsyncWebsocketConsumer):
    """Handle real-time room-based chat over WebSockets."""

    async def connect(self):
        """Join the requested chat room and accept the WebSocket connection."""
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )

        await self.accept()

    async def disconnect(self, close_code):
        """Leave the chat room when the socket disconnects."""
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )

    async def receive(self, text_data):
        """Receive a message from the browser, save it, and broadcast it."""
        data = json.loads(text_data)
        message = data.get("message", "").strip()

        if not message:
            return

        user = self.scope.get("user")
        if not user or isinstance(user, AnonymousUser) or not user.is_authenticated:
            return

        # Save the message to the database.
        saved_message = await self.save_chat_message(
            room_name=self.room_name,
            user=user,
            message=message,
        )

        # Broadcast the saved message to all users in the room.
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": saved_message["message"],
                "username": saved_message["username"],
                "timestamp": saved_message["timestamp"],
            },
        )

    async def chat_message(self, event):
        """Send a broadcast message back to all clients in the room."""
        await self.send(
            text_data=json.dumps(
                {
                    "message": event["message"],
                    "username": event["username"],
                    "timestamp": event["timestamp"],
                }
            )
        )

    @database_sync_to_async
    def save_chat_message(self, room_name, user, message):
        """Persist a chat message and return serialized values."""
        chat_message = ChatMessage.objects.create(
            room_name=room_name,
            user=user,
            message=message,
        )
        return {
            "message": chat_message.message,
            "username": chat_message.user.username,
            "timestamp": chat_message.timestamp.strftime("%b %d, %Y %H:%M"),
        }