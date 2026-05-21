from rest_framework import viewsets, permissions
from .models import Subject, Test
from .serializers import SubjectSerializer, TestSerializer

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [permissions.AllowAny] # Change to IsAuthenticated later if needed

class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all().order_by('-created_at')
    serializer_class = TestSerializer
    permission_classes = [permissions.AllowAny] # Change to IsAuthenticated later if needed
