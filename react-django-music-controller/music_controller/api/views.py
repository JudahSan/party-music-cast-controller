from django.shortcuts import render
# from django.http import HttpResponse
from rest_framework import generics
from .serializers import RoomSerializer #CreateRoomSerializer
from .models import Room
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.
"""
# Return response function
def main(request):
	return HttpResponse("<h1>Bonjour</h1>")
"""

# Create an API view that lets us view a list of all
#  the different rooms

class RoomView(generics.ListAPIView):
	queryset = Room.objects.all()
	serializer_class = RoomSerializer

