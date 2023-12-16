from django.utils import timezone
from client.models import Event  # Import the Event model from your Django app
from django.core.cache import cache
from django.core.serializers.json import DjangoJSONEncoder
from celery import shared_task
import json
from django.forms.models import model_to_dict
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

import requests
@shared_task(rate_limit='1000/s')
def send_log_data_to_server(name_data ):
    # Assuming log_data is a dictionary with the provided fields
    try:
    # Filter the Event objects based on the criteria
        # queryset = Event.objects.filter(
        #     stream_id = name_data['stream_id'],
        #     timestamp = name_data['timestamp'],
        #     status = name_data['status'],
        #     session_id = name_data['session_id'],
        #     log_type = name_data['log_type'],
        #     log_coordinates = name_data['log_coordinates'],
        #     log_thumbnail = name_data['log_thumbnail'],
        # 
        log_instance = {
            'stream_id': name_data['stream_id'],
            'timestamp': str(name_data['timestamp']),
            'status': name_data['status'],
            'session_id': str(name_data['session_id']),
            'log_type': name_data['log_type'],
            'log_coordinates': name_data['log_coordinates'],
            'log_thumbnail': name_data['log_thumbnail'],
        }

        # Serialize the log_instance data
        serialized_data = json.dumps(log_instance ,cls=DjangoJSONEncoder)
        print(serialized_data, " hbahhilfeofeoiweir8r949houerfoerjfojererjobve")

        # Rest of your code...
        url = 'http://127.0.0.1:8000/event/' 
        payload = {'data': json.loads(serialized_data)}
        
        print("7777777777777777777777777777777777", payload, "8888888888888888888888888888888")

        response = requests.post(url=url, json=payload)
        print(response, "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        cache.set("rule", response)
        # Process the response or perform additional actions
        
            # Handle the response data as needed
        

    except ObjectDoesNotExist:
        # Handle the case where no matching object is found
        return {'error': 'No matching Event object found.'}