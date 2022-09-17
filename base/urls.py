from django.urls import path,include
from base import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("lobby/<int:room_id>/",views.Lobby,name="lobby"),
    path("",views.Home,name="home"),
    path("login/",views.Login,name="login"),
    path("logout/",views.Logout,name="logout"),
    path("register/",views.Register,name="register"),
    path("send-message/",views.SendMessage,name="send-message"),
    path("add-chat/",views.AddChat,name="add-chat"),
    path("edit-chat/<int:pk>/",views.EditChat,name="edit-chat"),


]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)