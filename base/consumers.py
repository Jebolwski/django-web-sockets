from cmath import log
import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

botName = "ChatBot"

class ChatConsumer(WebsocketConsumer):
    def connect(self):

        room_id = self.scope.get('url_route').get('kwargs').get('room_id')
        if self.scope["user"].is_anonymous:
            self.close()

        username = self.scope['user'].username

        print(self.scope['user'],"is connected.")
        self.accept()
        self.room_group_name = room_id

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type':'botJoinMessage',
                'message':username+" has joined the chat.",
                'sender':username,
            }
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        username = data.get('username')
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type':'chatMessage',
                'message':data.get('message'),
                'username':username,
            }
        )

    def disconnect(self,close_code):
        print("DISCONNECTED")

        username = self.scope["user"].username
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type':'botLeaveMessage',
                'message':username+" has left the chat."
            }
        )
        print(username+" has left this chat.")
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        self.close()
    
    def chatMessage(self,event):
        message = event.get('message')
        username = event.get('username')

        self.send(text_data=json.dumps({
            'type':'chat',
            'user': username,
            'message':message
        }))

    def botJoinMessage(self,event):
        message = event.get('message')
        sender = event.get('sender')

        self.send(text_data=json.dumps({
            'type':'botjoinmessagge',
            'user':botName,
            'sender':sender,
            'message':message
        }))

    def botLeaveMessage(self,event):
        message = event.get('message')
        sender = event.get('sender')

        self.send(text_data=json.dumps({
            'type':'botleavemessagge',
            'user':botName,
            'message':message
        }))
    

    