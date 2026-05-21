from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SubjectViewSet, TestViewSet

router = DefaultRouter()
router.register(r'subjects', SubjectViewSet)
router.register(r'list', TestViewSet, basename='test')

urlpatterns = [
    path('', include(router.urls)),
]
