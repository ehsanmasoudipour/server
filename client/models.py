from django.db import models

# Create your models here.

class Event(models.Model):
    """
    Represents an event in the system.
    """
    stream_id = models.IntegerField()
    """
    The ID of the stream associated with the event.
    """

    timestamp = models.DateTimeField()
    """
    The timestamp of the event.
    """

    status = models.CharField(max_length=1, choices=[('D', 'Danger'), ('S', 'Safe')])
    """
    The status of the event. 'D' represents danger and 'S' represents safe.
    """

    session_id = models.UUIDField()
    """
    The UUID of the session associated with the event.
    """
    log_type = models.CharField(max_length=10)
    """
    The type of object in the log. Possible values: 'Person', 'Face', 'Bag'.
    """

    log_coordinates = models.CharField(max_length=100)
    """
    The coordinates of the object in the log. A list of four integers.
    """

    log_thumbnail = models.TextField()
    """
    The base64-encoded image thumbnail of the object in the log.
    """
    


