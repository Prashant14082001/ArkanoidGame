# canvasApp/consumers.py
import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

class CanvasConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'canvas_{self.room_name}'

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        # Accept WebSocket connection
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        # Receive message from WebSocket
        text_data_json = json.loads(text_data)
        x = text_data_json['x']
        y = text_data_json['y']
        event_type = text_data_json['type']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'canvas_draw',
                'x': x,
                'y': y,
                'event_type': event_type,
                'sender_channel_name': self.channel_name  
            }
        )

    def canvas_draw(self, event):
        # Receive message from room group
        x = event['x']
        y = event['y']
        event_type = event['event_type']
        sender_channel_name = event['sender_channel_name']  

        # Send message to WebSocket
        if self.channel_name != sender_channel_name:  
            self.send(text_data=json.dumps({
                'x': x,
                'y': y,
                'type': event_type
            }))
