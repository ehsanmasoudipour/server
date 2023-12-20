from django.utils import timezone
from client.models import Event  # Import the Event model from your Django app
from django.core.cache import cache
from django.core.serializers.json import DjangoJSONEncoder
from celery import shared_task
import json
from django.forms.models import model_to_dict
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers.json import DjangoJSONEncoder
from celery import shared_task
import json
import requests

@shared_task(rate_limit='1000/s')
def send_log_data_to_server(name_data):
    try:
        log_instance = {
            'stream_id': name_data['stream_id'],
            'timestamp': str(name_data['timestamp']),
            'status': name_data['status'],
            'session_id': str(name_data['session_id']),
            'log_type': name_data['log_type'],
            'log_coordinates': name_data['log_coordinates'],
            
        }
        serialized_data = json.dumps(log_instance, cls=DjangoJSONEncoder)
        url = 'http://127.0.0.1:8000/event/' 
        payload = {'data': json.loads(serialized_data)}
        response = requests.post(url=url, json=payload)
        # Check if the request was successful (status code 2xx)
        if response.status_code // 100 == 2:
            return {'success': f'Task completed successfully for stream_id: {name_data["stream_id"]} timestamp: {name_data['timestamp']} status: {name_data['status']}session_id: {str(name_data['session_id'])} log_type: {name_data['log_type']} log_coordinates: {name_data['log_coordinates']}'}
        else:
            return {'error': f'Task failed with status code {response.status_code} for stream_id: {name_data["stream_id"]}'}

    except ObjectDoesNotExist as e:
        return {'error': f'No matching Event object found. Error: {e}'}

    except Exception as e:
        return {'error': f'An unexpected error occurred: {e}'}

