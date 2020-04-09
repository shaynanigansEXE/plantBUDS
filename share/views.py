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
    # print('*********** Testing request obj ************')
    # print('request:' , request)
    # print('request.headers: ', request.headers)
    # print('request.headers["host"]:', request.headers['host'])
    # print('request.method: ', request.method)
    # print('request.user:' , request.user)
    # print('*******************************')

    if request.method == "GET":
        user = request.user
        if not user.is_authenticated:
            return redirect("share:login")
        else:
            # my_posts = Posts.objects.filter(publisher=user.publisher.id)   # Posts table has a publisher field (FK)

            # print('*********** Testing objs retrieved from DB ************')
            # # print('my_posts:', my_posts)
            # print('*******************************')
            return render(request, "share/dashboard.html")
            # return render(request, "share/dashboard.html", {'my_posts':my_posts})

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

'''

def show_post(request, publisher_id):
    if request.method == "GET":
        user = request.user
        if not user.is_authenticated:
            return redirect("share:login")
        else:
            # make sure to import the fucntion get_object_or_404 from  django.shortcuts
            post = get_object_or_404(Post, pk=publisher_id)

            if post.publisher.user.id == user.id or post.make_public:
                return render(request, "share/posts.html",
                {"user":user, "post":post})
            else:
                # you are not the author
                all_posts = Posts.objects.all()
                return render(request, "share/index.html",
                {"user":user, "all_posts": all_posts, "error":"The post you clicked is not public and you are not the author"})
'''

def edit_post(request, publisher_id):
    if request.method == "GET":
        user = request.user
        if not user.is_authenticated:
            return redirect("share:login")

        post = get_object_or_404(Posts, pk=publisher_id)

        if post.publisher.user.id == user.id:
            return render(request, "share/publish_post.html", {"publisher":publisher})
        else:
            return render(request, "share/index.html",
            {"error":"You are not the author of the post that you tried to edit."})

def update_post(request, publisher_id):
    if request.method == "POST":
        user = request.user
        if not user.is_authenticated:
            return HttpResponse(status=500)

        post = get_object_or_404(Posts, pk=publisher_id)

        if not request.POST["title"] or not request.POST["description"] or not request.POST["subject"]:
            return render(request, "share/publish_post.html", {"publisher":publisher,
            "error":"One of the required fields was empty"})

        else:
            publisher = user.publisher
            title = request.POST["title"]
            description = request.POST["description"]
            subject = request.POST["subject"]
            body = request.POST["body"]

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

            if post.publisher.user.id == user.id and not post.make_public:
                Posts.objects.filter(pk=publisher_id).update(publisher= publisher, title=title, description=description, subject=subject, body=body, make_public=make_public)
                return redirect("share:dashboard")

            else:
                return render(request, "share/publish_post.html",{"publisher":publisher, "error":"Can't update!"})

    else:
        # the user enteing    http://127.0.0.1:8000/problem/8/update
        user = request.user
        all_posts = Posts.objects.all()
        return render(request, "share/index.html", {"user":user, "all_posts": all_posts, "error":"Can't update!"})

def delete_post(request, publisher_id):
    if request.method == "GET":
        user = request.user
        if not user.is_authenticated:
            return HttpResponse(status=500)

        post = get_object_or_404(Posts, pk=publisher_id)

        if post.publisher.user.id == user.id and not post.make_public:
            Posts.objects.get(pk=publisher_id).delete()
            return redirect("share:dashboard")
        else:
            all_posts = Posts.objects.all()
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

        publisher = user.publisher
        title = request.POST["title"]
        description = request.POST["description"]
        subject = request.POST["subject"]
        body = request.POST["body"]

        make_public = request.POST.get('make_public', False)
        if make_public == 'on':
            make_public = True
        else:
            make_public = False

        if not title and not description:
            return render(request, "share/publish_post.html", {"error":"Please fill in all required fields"})

        try:
            post = Posts.objects.create(publisher=publisher, title=title, description=description, subject=subject, body=body, make_public=make_public)
            post.save()

            post = get_object_or_404(Posts, pk=publisher.id)

            return render(request, "share/dashboard.html",{"user":user, "post":post})

        except:
            return render(request, "share/publish_post.html", {"error":"Can't create the post"})

    else:
        # the user enteing    http://127.0.0.1:8000/problem/8/create
        user = request.user
        all_posts = Posts.objects.all()
        return render(request, "share/index.html", {"user":user, "all_posts": all_posts, "error":"Can't create!"})
