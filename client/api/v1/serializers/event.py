from rest_framework import serializers
from client.models import Event
class EventSerializer(serializers.ModelSerializer):


   class Meta:
        model = Event
        fields = ['stream_id', 'timestamp', 'status','log_type', 'log_coordinates','session_id']
