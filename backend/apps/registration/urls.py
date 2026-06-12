from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ParticipantViewSet, OperatorViewSet, public_register, get_by_id, public_operators

router = DefaultRouter()
router.register(r'participants', ParticipantViewSet)
router.register(r'operators', OperatorViewSet)

urlpatterns = [
    path('operators/public/', public_operators, name='public-operators'),
    path('', include(router.urls)),
    path('register/', public_register, name='public-register'),
    path('get_by_id/', get_by_id, name='get-by-id'),
]
