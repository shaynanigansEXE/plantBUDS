# import three functions: authentication, login, logout
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from .models import PlantTip, PlantBuddy, Publishing
from django.contrib.auth.models import User
from django.http import HttpResponse

def index(request):
    # request for user authentication
    if request.method == "GET":
        all_posts = Publishing.objects.all()   # all_problems is a list object [   ]

        return render(request, "share/index.html", {'all_posts':all_posts})
    else:
        return redirect("share:login")
'''
    else:
        return HttpResponse(status=500)
'''
def dashboard(request):
    if request.method == "GET":
        user = request.user
        if not user.is_authenticated:
            return redirect("share:login")
        else:
            my_posts = Publishing.objects.filter(plantbuddy=user.plantbuddy.id)   # Posts table has a plantbuddy field (FK)

            print('*********** Testing objs retrieved from DB ************')
            print('my_posts:', my_posts)
            print('*******************************')

            return render(request, "share/dashboard.html", {'my_posts':my_posts})

def info_page(request):
    # request for user authentication
    if request.method == "GET":
        return render(request, "share/info_page.html")
    else:
        return redirect("share:login")
'''    else:
        return HttpResponse(status=500)
'''
def signup(request):
    if request.user.is_authenticated:
        return redirect("share:index")
    return render(request, 'share/signup.html')

def create(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        farm_pro = True

        if username is not None and email is not None and password is not None: # checking that they are not None
            if not username or not email or not password: # checking that they are not empty
                return render(request, "share/signup.html", {"error": "Please fill in all required fields"})
            if User.objects.filter(username=username).exists():
                return render(request, "share/signup.html", {"error": "Username already exists"})
            elif User.objects.filter(email=email).exists():
                return render(request, "share/signup.html", {"error": "Email already exists"})
            # save our new user in the User model
            user = User.objects.create_user(username, email, password)
            plantbuddy = PlantBuddy.objects.create(user=user, farm_pro = farm_pro).save()
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
    return redirect("share:index")

def show_posts(request, plantbuddy_id):
    if request.method == "GET":
        user = request.user
        if not user.is_authenticated:
            return redirect("share:login")
        else:
            # make sure to import the fucntion get_object_or_404 from  django.shortcuts
            my_posts = get_object_or_404(Publishing, pk=plantbuddy_id)

            # Module 6
            if my_posts.make_public or my_posts.plantbuddy.user.id == user.id:
                return render(request, "share/show_posts.html", {"user":user, "my_posts":my_posts})
            else:
                # the problem is private and you are not the author
                return render(request, "share/index.html",
                {"error":"The post you clicked is still private and you are not the author"})

def farmer_posts(request):
    '''
        if request.method == "GET":
            if request.user.is_authenticated:
                user = request.user
                all_posts = Publishing.objects.all()   # all_problems is a list object [   ]

                return render(request, "share/farmer_posts.html", {"user":user, "all_posts": all_posts})
            else:
                return redirect("share:login")
        else:
            return HttpResponse(status=500)
    '''
    if request.method == "GET":
        user = request.user
        if not user.is_authenticated:
            return redirect("share:login")
        else:
            my_posts = Publishing.objects.filter(plantbuddy=user.plantbuddy.id)   # Posts table has a plantbuddy field (FK)

            print('*********** Testing objs retrieved from DB ************')
            print('my_posts:', my_posts)
            print('*******************************')

            return render(request, "share/farmer_posts.html", {'my_posts':my_posts})


def edit_post(request, plantbuddy_id):
    if request.method == "GET":
        user = request.user
        if not user.is_authenticated:
            return redirect("share:login")

        my_post = get_object_or_404(Publishing, pk=plantbuddy_id)


        if my_post.plantbuddy.user.id == user.id:
            return render(request, "share/edit_post.html", {"my_post":my_post})
        else:
            return render(request, "share/index.html",
            {"error":"You are not the author of the problem that you tried to edit."})

# Module 6
def update_post(request, plantbuddy_id):
    if request.method == "POST":
        user = request.user
        if not user.is_authenticated:
            return HttpResponse(status=500)

        my_post = get_object_or_404(Publishing, pk=plantbuddy_id)

        if not request.POST["title"] or not request.POST["description"] or not request.POST["body"] or not request.POST["subject"]:
            return render(request, "share/edit_post.html", {"my_post":my_post, "error":"One of the required fields was empty"})

        else:
            title = request.POST["title"]
            description = request.POST["description"]
            body = request.POST["body"]
            subject = request.POST["subject"]

            make_public = request.POST.get('make_public', False)

            print('***********************')
            print('user input make_public:', make_public)    # it shows as on

            if make_public == 'on':
                make_public = True
            else:
                make_public = False

            print('******** Testing *************')
            print('make_public:', make_public)
            print('***********************')

            if my_post.plantbuddy.user.id == user.id and not my_post.make_public:
                Publishing.objects.filter(pk=plantbuddy_id).update(title=title, description=description, body=body, subject=subject, make_public=make_public)
                return redirect("share:dashboard")

            else:
                return render(request, "share/edit_post.html",{"my_post":my_post, "error":"Can't update!"})

    else:
        # the user enteing    http://127.0.0.1:8000/problem/8/update
        user = request.user
        all_posts = Publishing.objects.all()
        return render(request, "share/index.html", {"user":user, "all_posts": all_posts, "error":"Can't update!"})

def delete_post(request, plantbuddy_id):
    if request.method == "GET":
        user = request.user
        if not user.is_authenticated:
            return HttpResponse(status=500)

        my_post = get_object_or_404(Publishing, pk=plantbuddy_id)

        if my_post.plantbuddy.user.id == user.id and not my_post.make_public:
            Publishing.objects.get(pk=plantbuddy_id).delete()
            return redirect("share:dashboard")
        else:
            all_posts = Publishing.objects.all()
            return render(request, "share/index.html", {"user":user, "all_posts": all_posts, "error":"Can't delete!"})

    else:
        return HttpResponse(status=500)

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

        plantbuddy = user.plantbuddy
        title = request.POST["title"]
        description = request.POST["description"]
        subject = request.POST["subject"]
        body = request.POST["body"]
        make_public = request.POST.get('make_public', False)
        if make_public == 'on':
            make_public = True
        else:
            make_public = False

        if not title and not description and not body:
            return render(request, "share/publish_post.html", {"error":"Please fill in all required fields"})

        try:
            post = Publishing.objects.create(plantbuddy=plantbuddy, title=title, description=description, subject=subject, body=body, make_public=make_public)
            post.save()

            post = get_object_or_404(Publishing, pk=plantbuddy.id)

            return render(request, "share/farmer_posts.html",{"user":user, "post":post})

        except:
            return render(request, "share/publish_post.html", {"error":"Can't create the problem"})

    else:
        # the user enteing    http://127.0.0.1:8000/problem/8/create
        user = request.user
        all_posts = Publishing.objects.all()
        return render(request, "share/index.html", {"user":user, "all_posts": all_posts, "error":"Can't create!"})
