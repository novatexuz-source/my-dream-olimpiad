from django.urls import path
from .views import ResultsListView

urlpatterns = [
    path('', ResultsListView.as_view(), name='results_list'),
]
