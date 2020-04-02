# import three functions: authentication, login, logout
from django.contrib.auth import authenticate, login, logout
# import redirect
from django.shortcuts import render, redirect
# import all the models created so far
from .models import PlantTip, PlantBuddy
# import User model
from django.contrib.auth.models import User
from django.http import HttpResponse


def base(request):
    # Testing http request object inside a view function

    # request for user authentication
    if request.method == "GET":
        if request.user.is_authenticated:
            user = request.user
            return render(request, "share/login.html", {"user":user})
        else:
            return redirect("share:base")
    else:
        return HttpResponse(status=500)

def dashboard(request):
    # retieve user
    # renders learn_more.html
    # Testing http request object inside a view function
    # Testing http request object inside a view function
    if request.method == "GET":
        user = request.user
        if not user.is_authenticated:
            return redirect("share:login")
        else:
            return render(request, "share/dashboard.html")

def signup(request):
    if request.user.is_authenticated:
        return redirect("share:dashboard")
    return render(request, 'share/signup.html')

def create(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        farm_pro = request.POST['farm_pro_checkbox']

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
            return redirect("share:dashboard")
        else:
            return render(request, "share/login.html", {"error":"Wrong username or password"})
    else:
        return redirect("share:base")


def logout_view(request):
    logout(request)
    return redirect("share:base")

'''
def posts(request):
    if request.method == "GET":
        user = request.user
        if not user.is_authenticated:
            return redirect("share:login")
        else:
            # make sure to import the fucntion get_object_or_404 from  django.shortcuts
            title = get_object_or_404(Problem, pk=problem_id)
            text = Script.objects.filter(problem=problem_id)

            return render(request, "share/problem.html", {"user":user, "title":problem, "scripts": scripts})
'''
