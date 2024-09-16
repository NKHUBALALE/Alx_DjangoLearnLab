# blog/urls.py
from django.urls import path
from .views import register_page, login_page, logout_page, profile_page

urlpatterns = [
    path('register/', register_page, name='register'),
    path('login/', login_page, name='login'),
    path('logout/', logout_page, name='logout'),
    path('profile/', profile_page, name='profile'),
]