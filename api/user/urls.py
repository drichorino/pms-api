from django.urls import path
from . import views

urlpatterns = [

    path("login/", views.login, name='login'),
    path("logout/", views.logout, name='logout'),
    
    path("create-user/", views.add_users, name='create-user'),
    path("current-user/", views.current_user, name='current-user'),   
    path("delete-user/", views.delete_user, name='delete-user'),   
    path("restore-user/", views.restore_user, name='restore-user'),   
    path("list-users/", views.list_users, name='list-users'),   
    path("archived-users/", views.list_archived_users, name='archived-users'),   
]
