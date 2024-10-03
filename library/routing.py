from django.urls import path
from .consumers import BookAvailabilityConsumer

websocket_urlpatterns = [
    path("ws/book-availability/", BookAvailabilityConsumer.as_asgi()),
]