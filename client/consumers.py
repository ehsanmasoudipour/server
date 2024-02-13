
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json 

class TestConsumer(WebsocketConsumer):
    
    def connect(self):
        self.room_group_name = "test_consumer_group"
        
        # Add this consumer to the group when connected
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        
        self.accept()
        self.send(text_data=json.dumps({'status': 'connected from Django project socket testing'}))
        
    def receive(self, text_data):
        print(text_data)
        self.send(text_data=json.dumps({'status': 'we got you'}))
    
    def disconnect(self, close_code):
        # Remove this consumer from the group when disconnected
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        
    def send_notification(self, event):
        data = json.loads(event['value'])
        self.send(text_data=json.dumps({'payload': data}))
