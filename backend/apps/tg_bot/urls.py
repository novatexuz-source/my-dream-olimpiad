from django.urls import path

from . import views

urlpatterns = [
    path('webhook/<str:token>/', views.telegram_webhook, name='tg_webhook'),
    path('set-webhook/<str:token>/', views.set_webhook, name='tg_set_webhook'),
]
