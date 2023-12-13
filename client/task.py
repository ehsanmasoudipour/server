from celery import shared_task
import json
import requests
from client.models import Event
from django.core.cache import cache

@shared_task()
def task_execute(job_params):

    event = Event.objects.get(pk=job_params["db_id"])
    cache.set('processed_data_key', event)
    event.save()
    
    
@shared_task
def send_log_data_to_server(log_data):
    # Assuming log_data is a dictionary with the provided fields
    stream_id = log_data.get('stream_id')
    timestamp = log_data.get('timestamp')
    status = log_data.get('status')
    session_id = log_data.get('session_id')
    log_type = log_data.get('log_type')
    log_coordinates = log_data.get('log_coordinates')
    log_thumbnail = log_data.get('log_thumbnail')

    # Save the log data to your Django model (optional)
    log_instance = Event.objects.create(
        stream_id=stream_id,
        timestamp=timestamp,
        status=status,
        session_id=session_id,
        log_type=log_type,
        log_coordinates=log_coordinates,
        log_thumbnail=log_thumbnail
    )
    
    url = 'http://127.0.0.1:6379/event/api/service/'  # Update with your actual URL
    payload = {'data': json.dumps(log_data)}

    response = requests.post(url, data=payload)

    return response.json()