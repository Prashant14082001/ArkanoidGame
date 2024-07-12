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



from channels.generic.websocket import AsyncWebsocketConsumer
import json

class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'game_{self.room_name}'
        
        self.user = self.scope['user']  # Assuming you are using Django authentication
        self.is_controller = False

        # Add the user to the room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Check if there is already a controller in the room
        if not hasattr(self.channel_layer, 'controllers'):
            self.channel_layer.controllers = {}

        if self.room_group_name not in self.channel_layer.controllers:
            self.channel_layer.controllers[self.room_group_name] = self.channel_name
            self.is_controller = True

        await self.accept()

        # Send initial game state to the new connection
        await self.send(text_data=json.dumps({
            'controller': self.is_controller
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        
        if self.is_controller:
            del self.channel_layer.controllers[self.room_group_name]
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'controller_left',
                    'message': 'The controller has left the room.'
                }
            )
            

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type', None)

        if message_type == 'game_state':
            game_state = data.get('game_state', None)
            if game_state and self.channel_name == self.channel_layer.controllers.get(self.room_group_name):
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'game_state_update',
                        'game_state': game_state
                    }
                )
        elif message_type == 'chat_message':
            message = data.get('message', '')
            username = self.user.username
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'username': username
                }
            )

    async def game_state_update(self, event):
        game_state = event['game_state']

        # Send game state to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'game_state',
            'game_state': game_state
        }))
    
    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        # Send chat message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': message,
            'username': username
        }))
        
    async def controller_left(self, event):
        message = event['message']

        # Send controller left message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'controller_left',
            'message': message
        }))

