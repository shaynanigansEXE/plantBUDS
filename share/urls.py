from django.urls import path, include
from . import views  #import everything from views module

app_name = 'share'

urlpatterns = [
    # Most redirects lead here if user has been authenticated
    path('', views.index, name='index'),

    # authentication: signup, login, logout
    path('create', views.create, name='create'),
    path('loguser', views.login_user, name='loguser'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('signup', views.signup, name='signup'),
    path('dashboard', views.dashboard, name='dashboard'),

#    path('post/<int:publisher_id>/show', views.show_post, name='show_post'),
    path('post/<int:publisher_id>/edit', views.edit_post, name='edit_post'),
    path('post/<int:publisher_id>/update', views.update_post, name='update_post'),
    path('post/<int:publisher_id>/delete', views.delete_post, name='delete_post'),

    path('publish_post', views.publish_post, name='publish_post'),
    path('create_post', views.create_post, name='create_post'),
]
