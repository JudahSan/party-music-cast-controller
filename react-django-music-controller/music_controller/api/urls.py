from django.urls import path
from .views import main #RoomView, CreateRoomView

urlpatterns = [
    path('home', main),
    path('', main)
]
