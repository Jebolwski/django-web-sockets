from django.urls import path,include
from base import views

urlpatterns = [
    path("lobby/",views.Lobby,name="lobby"),
]