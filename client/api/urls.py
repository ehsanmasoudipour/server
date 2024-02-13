from django.urls import path
from ..api.v1.views import EventApiView
from ..api.v1.views import event
urlpatterns = [
    path('create_api/', EventApiView.as_view(), name='your-view-name'),
    path('create_session/', EventApiView.dbco, name='session'),
    # path("", event.index, name="index"),
    path('home/', event.home)
    # Add more patterns as needed
]

