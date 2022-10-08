from django.urls import path
from . import views

urlpatterns = [

    path("login/", views.login, name='login'),
    path("logout/", views.logout, name='logout'),
    
    path('create-user/', views.add_users, name='create-user'),
    path("current-user/", views.current_user, name='current-user'),   
]
