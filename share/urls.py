from django.urls import path, include
from . import views  #import everything from views module

app_name = 'share'

urlpatterns = [
    # Most redirects lead here if user has been authenticated
    path('', views.base, name='base'),

    # authentication: signup, login, logout
    path('create', views.create, name='create'),
    path('loguser', views.login_user, name='loguser'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('signup', views.signup, name='signup'),
    path('learn_more', views.learn_more, name='learn_more'),
    #path('posts', views.posts, name='posts')
]
