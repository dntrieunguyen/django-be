# user/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.get_all_users, name='get_all_users'),
    path('users/detail', views.get_user, name='get_user'),
    path('users/create/', views.create_user, name='create_user'),
    path('users/<uuid:id>/update/', views.update_user, name='update_user'),
    path('users/<uuid:id>/delete/', views.delete_user, name='delete_user'),
]
