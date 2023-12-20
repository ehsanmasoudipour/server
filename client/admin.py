# admin.py
from django.contrib import admin

from .models import Event
from django.utils.html import mark_safe
from .models import Event
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        'stream_id',
        'timestamp',
        'status',
        'session_id',
        'log_type',
        'log_coordinates',
    )