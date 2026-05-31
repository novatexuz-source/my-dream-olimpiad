from django.urls import path
from .views import ResultsListView, AttendanceListView, CertificateToggleView

urlpatterns = [
    path('', ResultsListView.as_view(), name='results_list'),
    path('attendance/', AttendanceListView.as_view(), name='attendance_list'),
    path('<uuid:session_id>/certificate/', CertificateToggleView.as_view(), name='certificate_toggle'),
]
