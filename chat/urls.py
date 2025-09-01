# chat/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("text/", views.chatbot, name="chatbot_text"),
    path("voice/", views.chatbot, name="chatbot_voice"),
]
