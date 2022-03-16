from django.urls import path
from .views import RoomView #CreateRoomView

urlpatterns = [
    path('home', RoomView.as_view()),
]
