from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ParticipantViewSet, public_register, get_by_id

router = DefaultRouter()
router.register(r'participants', ParticipantViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', public_register, name='public-register'),
    path('get_by_id/', get_by_id, name='get-by-id'),
]
