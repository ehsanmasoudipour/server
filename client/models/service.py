from django.db import models
import base64
from django.utils.translation import gettext_lazy as _
from django.core.files.base import ContentFile
# Create your models here.

class Event(models.Model):
    """
    this is class Event with deferrent field and  usin model django for each field .for some field  you need  install special
    package like pillow for image
    """
    stream_id = models.IntegerField(
        _("stream_id"),
        unique = True,
        help_text = _("stream id is an integer field ")    
    )
    
    timestamp = models.DateTimeField(
        _("timestamp"),
        help_text=_("data for each event.")
    )

    status = models.CharField(
        _("status"),
        max_length=1, 
        choices=[('D', 'Danger'),
                 ('S', 'Safe')],
        help_text = _(" status has two choices: D is for danger event and S is for safe event. ")
        )
    
    session_id = models.UUIDField(
        _("session_id"),
        unique = True,
        help_text = _("this is uuid field .")
        )
        
    log_type = models.CharField(
         _("log_type"),
        max_length=10,
        choices=[('P','Person'),
                 ('F', 'Face'),
                 ('B','Bag')],
         help_text = _(" you have to choose one of these for complete an event.")
        )
    
    log_coordinates = models.JSONField(
        _("log_coordinates"), 
        default=list,
        help_text = _("this field include four list of integer ")
        )  
    
    thumbnail = models.ImageField(
        _("Thumbnail"),
        upload_to='client/media/',
        blank=True,
        null=True,
        help_text = _("this is a image and it is encoded with base64")
    )
    
    def save_thumbnail_from_base64(self):
        if self.thumbnail:
            format, imgstr = self.thumbnail.split(';base64,')  # Split the string into format and data
            ext = format.split('/')[-1]  # Extract the file extension
            data = ContentFile(base64.b64decode(imgstr), name=f'thumbnail.{ext}')
            self.thumbnail.save(f'thumbnail.{ext}', data, save=True)
            self.thumbnail = None  # Clear the Base64 field after saving

    def save(self, *args, **kwargs):
        self.save_thumbnail_from_base64()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.stream_id} - {self.timestamp} - {self.status} - {self.session_id} - {self.log_type}"

    class Meta:
        verbose_name = _("Event")
        verbose_name_plural = _("Events")


