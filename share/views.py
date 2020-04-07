# import three functions: authentication, login, logout
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from .models import PlantBuddy, Posts
from django.contrib.auth.models import User
from django.http import HttpResponse


def index(request):
    # request for user authentication
    if request.method == "GET":
        if request.user.is_authenticated:
            user = request.user
            all_posts = Posts.objects.all()   # all_problems is a list object [   ]

            return render(request, "share/index.html", {"user":user, 'all_posts':all_posts})
        else:
            return redirect("share:login")
    else:
        return HttpResponse(status=500)

def dashboard(request):
    print('*********** Testing request obj ************')
    print('request:' , request)
    print('request.headers: ', request.headers)
    print('request.headers["host"]:', request.headers['host'])
    print('request.method: ', request.method)
    print('request.user:' , request.user)
    print('*******************************')

    if request.method == "GET":
        user = request.user
        if not user.is_authenticated:
            return redirect("share:login")
        else:
#            my_posts = Posts.objects.filter(publisher=user.publisher.id)   # Posts table has a publisher field (FK)

            return render(request, "share/dashboard.html")

def signup(request):
    if request.user.is_authenticated:
        return redirect("share:index")
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
            publisher = PlantBuddy.objects.create(user= user, farm_pro = farm_pro).save()
            user.save()

            login(request, user, backend="django.contrib.auth.backends.ModelBackend")
            # this logs in our new user, backend means that we are using the  Django specific auhentication and not 3rd party

        return redirect("share:index")

    else:
        return redirect("share:signup")

def login_view(request):
    if request.user.is_authenticated:
        return redirect("share:index")
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
        return redirect("share:index")

def logout_view(request):
    logout(request)
    return redirect("share:login")

def publish_post(request):
    if request.method == "GET":
        user = request.user
        if not user.is_authenticated:
            return redirect("share:login")
        else:
            return render(request, "share/publish_post.html", {"user":user} )

def create_post(request):
    if request.method == "POST":
        user = request.user
        if not user.is_authenticated:
            return redirect("share:login")

        publisher = user.publisher
        title = request.POST["title"]
        description = request.POST["description"]
        discipline = request.POST["discipline"]
        make_public = request.POST.get('make_public', False)
        if make_public == 'on':
            make_public = True
        else:
            make_public = False

        if not title and not description:
            return render(request, "share/publish_post.html", {"error":"Please fill in all required fields"})

        try:
            post = Posts.objects.create(publisher=publisher, title=title, description=description, discipline=discipline, make_public=make_public)
            post.save()

            post = get_object_or_404(Posts, pk=publisher.id)

            return render(request, "share/problem.html",{"user":user, "post":post})

        except:
            return render(request, "share/publish_problem_form.html", {"error":"Can't create the problem"})

    else:
        # the user enteing    http://127.0.0.1:8000/problem/8/create
        user = request.user
        all_posts = Posts.objects.all()
        return render(request, "share/index.html", {"user":user, "all_posts": all_posts, "error":"Can't create!"})
