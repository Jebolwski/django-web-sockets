import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.room_group_name = 'oda'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        
    def receive(self, text_data):
        data = json.loads(text_data)

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type':'chatMessage',
                'message':data.get('message')
            }
        )

    def chatMessage(self,event):
        message = event['message']

        self.send(text_data=json.dumps({
            'type':'chat',
            'message':message
        }))