from django.db import transaction

from rest_framework import viewsets, status
from rest_framework.exceptions import APIException
# from client.task import task_execute
from client.models import Event
from ..serializers import EventSerializer

from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from client.tasks import send_log_data_to_server
    

class EventApiView(APIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    allowed_methods = ['POST', 'GET']
    
    def post(self, request):
        
        data = EventSerializer(data=request.data)
        if data.is_valid():
            instance = data.save()
            instance.save()
            data_json = {
                'stream_id': instance.stream_id,
                'timestamp': instance.timestamp,
                'status': instance.status,
                'session_id': instance.session_id,
                'log_type': instance.log_type,
                'log_coordinates': instance.log_coordinates,
            }
            print("Data to be sent to Celery:", data_json)
            send_log_data_to_server.delay(data_json)
        return Response(data.data, status=status.HTTP_201_CREATED)



