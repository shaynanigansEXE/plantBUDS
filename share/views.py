from django.shortcuts import render
from django.http import HttpResponse
from share.models import PlantTip

# iteration2-initial-view
def index(request):
    # Testing request object inside a view function
    print('***********Testing ************')
    print('request.header: ', request.headers['host'])
    print('request.header: ', request.method)
    print('request:' , request)
    print('*******************************')
    if request.method == "GET":
        return render(request, 'share/base.html')
