import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer

class MyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send(text_data=json.dumps({'message': 'Connected'}))

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        pring(channels.layers.get_channel_layer())
        print(text_data)
        await self.send(text_data=json.dumps({
            'message': text_data
        }))


class ChatConsumer(WebsocketConsumer):

    def connect(self):
        # Make a database row with our channel name
        Clients.objects.create(channel_name=self.channel_name)

    def disconnect(self, close_code):
        # Note that in some rare cases (power loss, etc) disconnect may fail
        # to run; this naive example would leave zombie channel names around.
        Clients.objects.filter(channel_name=self.channel_name).delete()

    def chat_message(self, event):
        # Handles the "chat.message" event when it's sent to us.
        self.send(text_data=event["text"])