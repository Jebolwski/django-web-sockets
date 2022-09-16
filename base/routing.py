from django.urls import re_path
from . import consumers


websocket_urlpatterns = [
    re_path('ws/socket-server/(?P<room_id>\w+)/$',consumers.ChatConsumer.as_asgi())
]