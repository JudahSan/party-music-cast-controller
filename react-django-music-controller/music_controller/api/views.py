from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

# Return response function

def main(request):
	return HttpResponse("<h1>Bonjour</h1>")
