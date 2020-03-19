from django.shortcuts import render
from django.http import HttpResponse
from share.models import PlantTip

# iteration2-initial-view
def index(request):
    # GET method requesting data
    if request.method == "GET":
        # HTTP response for the GET method renders a message
        return HttpResponse("Hello World!")

def index(request):
    if request.method == "GET":
        return render(request, 'share/index.html')  # new line
