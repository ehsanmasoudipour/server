from django.db import transaction
from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.exceptions import APIException
# from client.task import task_execute
from client.models import Event
from ..serializers import EventSerializer
# from client.models import Event
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from client.tasks import send_log_data_to_server
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import json

class EventApiView(APIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    allowed_methods = ['POST', 'GET']
    permission_classes = [IsAuthenticated]
    
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

    def dbco(request):
        instance = Event.objects.all()
        
        request.sessions['Eevnt_data'] = {
            'stream_id': instance.stream_id,
            'timestamp': instance.timestamp,
            'status': instance.status,
            'session_id': instance.session_id,
            'log_type': instance.log_type,
            'log_coordinates': instance.log_coordinates,
        }
        stored_data = request.sessions.get('Event_data', {})
        return JsonResponse({'stored_data': stored_data})

# class ServerResponse(APIView):
    # permission_classes = [IsAuthenticated]
# 
    # def get(self, request, *args, **kwargs)
        # ... existing code

import time
def index(request):
    return render(request, "/client/template/index.html")


def home(request):
    for i in range(1, 10):
        channel_layer = get_channel_layer
        data = {'count': i}
        async_to_sync(channel_layer.group_send)(
            'test_consumer_group',
            {
                'type': 'send_notification',
                'value': json.dumps(data)
            }
        )
        time.sleep(1)
    return render(request, 'home.html')