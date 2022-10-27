from django.urls import path
from . import views

urlpatterns = [

    path("login/", views.login, name='login'),
    path("logout/", views.logout, name='logout'),
    
    path("users/create/", views.add_users, name='create-user'),
    path("users/current/", views.current_user, name='current-user'),
    path("users/update/", views.update_user, name='update-user'),   
    path("users/deactivate/", views.deactivate_user, name='deactivate-user'),   
    path("users/restore/", views.restore_user, name='restore-user'),   
    path("users/list/", views.list_users, name='list-users'),   
    path("users/archive/", views.list_archived_users, name='archived-users'),   
]
