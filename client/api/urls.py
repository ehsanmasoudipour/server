from rest_framework import routers
from client.api.v1.views import EventViewSet

router = routers.DefaultRouter()
router.register(r'Event', EventViewSet)

urlpatterns = router.urls


