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

# class EventViewSet(viewsets.ModelViewSet):

#     serializer_class = EventSerializer
#     queryset = Event.objects.all()

#     def perform_create(self, serializer):
#         try:
#             with transaction.atomic():
#                 # save instance
#                 instance = serializer.save()
#                 instance.save()

#                 # create task params
#                 job_params = {"db_id": instance.id}

#                 # submit task for background execution
#                 transaction.on_commit(lambda: task_execute.delay(job_params))

#         except Exception as e:
#             raise APIException(str(e))

# def some_view(request):
#     # Your data to be processed
#     data_to_process = 42

#     # Call the Celery task
#     task_execute.delay(data_to_process)
#     return HttpResponse("Task submitted for processing.")


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    allowed_methods = ['POST']
    

class EventApiView(APIView):
    # print("i am in class api view ")
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
                'log_thumbnail': instance.log_thumbnail,
            }

            # Print the data before sending it to Celery (for debugging)
            print("Data to be sent to Celery:", data_json)

            # Send data to Celery task
            send_log_data_to_server.delay(data_json)

            # return Response(data.data, status=status.HTTP_201_CREATED)
        # else:
        #     # Print serializer errors (for debugging)
        #     print("Serializer errors:", data.errors)
        #     return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(data.data, status=status.HTTP_201_CREATED)
    # except Exception as e:
    #     # Log any unexpected exceptions (for debugging)
    #     print(f"Unexpected error: {e}")
    #     return Response({"error": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        

  