"""
path: telegram_assistant/urls.py
"""

from django.urls import path
from . import views

app_name = 'telegram_assistant'

urlpatterns = [
    path('', views.monitor_view, name='monitor'),
    path('check-status/', views.check_status, name='check_status'),
    path('chats/', views.chats_view, name='chats'),
    path('api/chats/<int:chat_id>/messages/', views.api_messages, name='api_messages'),
]
