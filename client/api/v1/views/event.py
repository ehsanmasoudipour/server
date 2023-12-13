from django.db import transaction

from rest_framework import viewsets
from rest_framework.exceptions import APIException
from client.task import task_execute
from client.models import Event
from ..serializers import EventSerializer
from client.task import task_execute
from django.http import HttpResponse


class EventViewSet(viewsets.ModelViewSet):

    serializer_class = EventSerializer
    queryset = Event.objects.all()

    def perform_create(self, serializer):
        try:
            with transaction.atomic():
                # save instance
                instance = serializer.save()
                instance.save()

                # create task params
                job_params = {"db_id": instance.id}

                # submit task for background execution
                transaction.on_commit(lambda: task_execute.delay(job_params))

        except Exception as e:
            raise APIException(str(e))

def some_view(request):
    # Your data to be processed
    data_to_process = 42

    # Call the Celery task
    task_execute.delay(data_to_process)
    return HttpResponse("Task submitted for processing.")