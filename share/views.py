from django.shortcuts import render
from django.http import HttpResponse
from share.models import PlantTip

# Create your views here.
def index(request):
    if request.method == "GET":
        return HttpResponse("Hello World!")
