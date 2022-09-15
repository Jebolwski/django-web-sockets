from django.urls import path,include
from base import views

urlpatterns = [
    path("lobby/<slug:room_name>/",views.Lobby,name="lobby"),
    path("",views.Home,name="home"),
    path("login/",views.Login,name="login"),
    path("logout/",views.Logout,name="logout"),
    path("register/",views.Register,name="register"),
]