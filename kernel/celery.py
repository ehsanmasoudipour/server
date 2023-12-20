# from celery import shared_task
# import requests
# import json
# from client.models import Event

# # tasks.py

# from celery import shared_task
# import requests
# import json



#     # Now, you can send the data to your server using requests or any other method
#     url = 'http://192.168.1.1:6280/event/api/service/Event/'  # Update with your actual URL
#     payload = {'data': json.dumps(log_data)}

#     response = requests.post(url, data=payload)

#     return response.json()



import os

from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kernel.settings")

app = Celery("kernel")

app.config_from_object("django.conf:settings", namespace="CELERY")
# app.CELERY_TIMEZONE = 'Asia/tehran'
app.autodiscover_tasks()
