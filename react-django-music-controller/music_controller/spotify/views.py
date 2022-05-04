from django.shortcuts import render
from .credentials import REDIRECT_URI, CLIENT_SECRET, CLIENT_ID
from rest_framework.views import APIView
from requests import Request, post
from rest_framework import status
from rest_framework.response import Response
# Create your views here.

# setup API endpoint that'll return a url
# app authentication
class AuthURL(APIView):
    def get(self, request, format=None):
        # information we want to access from Spotify Docs
        scopes='user-read-playback-state user-modify-playback-state user-read-currently-playing'

        url = Request('GET', 'https://accounts.spotify.com/authorize', params={
            'scope': scopes,
            'response_type': 'code',
            'redirect_uri': REDIRECT_URI,
            'client_id': CLIENT_ID,
            # generate url for us
        }).prepare().url

        return Response({'url': url}, status=status.HTTP_200_OK)

