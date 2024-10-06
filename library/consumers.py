
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class BookAvailabilityConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "book_availability"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'book_availability_update',
                'message': message
            }
        )

    # will be used to send notifications to all connected clients when a book is returned.
    async def book_availability_update(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))
