from django.urls import path
from apps.exams import views

urlpatterns = [
    path('login/', views.exam_login, name='exam_login'),
    path('start/', views.start_exam, name='start_exam'),
    path('answer/', views.submit_answer, name='submit_answer'),
    path('finish/', views.finish_exam, name='finish_exam'),
    path('session/<uuid:session_id>/', views.get_exam_session, name='get_exam_session'),
    path('result/<uuid:session_id>/', views.get_exam_result, name='get_exam_result'),
]
