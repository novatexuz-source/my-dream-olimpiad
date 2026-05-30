from django.urls import path
from .views import ResultsListView, AttendanceListView

urlpatterns = [
    path('', ResultsListView.as_view(), name='results_list'),
    path('attendance/', AttendanceListView.as_view(), name='attendance_list'),
]
