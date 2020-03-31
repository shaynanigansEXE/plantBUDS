# import three functions: authentication, login, logout
from django.contrib.auth import authenticate, login, logout
# import redirect
from django.shortcuts import render, redirect
# import all the models created so far
from .models import PlantTip, PlantBuddy
# import User model
from django.contrib.auth.models import User

def index(request):
    # Testing http request object inside a view function

    # request for user authentication
    if request.method == "GET":
        if request.user.is_authenticated:
            user = request.user
            # # all_problems is a list object [ ]
            # all_problems = Problem.objects.all()

            return render(request, "share/base.html", {"user":user})
        else:
            return redirect("share:login")
    else:
        return HttpResponse(status=500)

def learn_more(request):
    # retieve user
    # renders dashboard.html
    # Testing http request object inside a view function

    if request.method == "GET":
        user = request.user
        if not user.is_authenticated:
            return redirect("share:login")
        else:
            return render(request, "share/learn_more.html")

def signup(request):
    if request.user.is_authenticated:
        return redirect("share:base")
    return render(request, 'share/signup.html')

def create(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        # # Had to make modifications because unchecked checkbox was throwing errors when submitting form
        # farm_pro = True
        # if request.POST.get and 'farm_pro' in request.POST and request.POST['farm_pro_checkbox'] == "False":
        #     farm_pro = False

        if username is not None and email is not None and password is not None: # checking that they are not None
            if not username or not email or not password: # checking that they are not empty
                return render(request, "share/signup.html", {"error": "Please fill in all required fields"})
            if User.objects.filter(username=username).exists():
                return render(request, "share/signup.html", {"error": "Username already exists"})
            elif User.objects.filter(email=email).exists():
                return render(request, "share/signup.html", {"error": "Email already exists"})
            # save our new user in the User model
            user = User.objects.create_user(username, email, password)
            plantbuddy = PlantBuddy.objects.create(user= user, farm_pro = farm_pro).save()
            user.save()

            login(request, user, backend="django.contrib.auth.backends.ModelBackend")
            # this logs in our new user, backend means that we are using the  Django specific auhentication and not 3rd party

        return redirect("share:base")

    else:
        return redirect("share:signup")

def login_view(request):
    if request.user.is_authenticated:
        return redirect("share:base")
    return render(request, 'share/login.html')

# the function loguser is called from the login form
def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        if not username or not password:
            return render(request, "share/login.html", {"error":"One of the fields was empty"})
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("share:base")
        else:
            return render(request, "share/login.html", {"error":"Wrong username or password"})
    else:
        return redirect("share:base")

def logout_view(request):
    logout(request)
    return redirect("share:login")
