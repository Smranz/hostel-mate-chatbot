from django.urls import path
from . import views

urlpatterns = [
    path("text/", views.text_chat, name="text_chat"),
    path("voice/", views.voice_chat, name="voice_chat"),
]
