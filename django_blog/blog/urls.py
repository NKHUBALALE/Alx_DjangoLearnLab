# blog/urls.py
from django.urls import path
from .views import ( 
    register_page, 
    login_page, 
    logout_page, 
    profile_page, 
    home_view,  
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
)   

urlpatterns = [
    path('', home_view, name='home'),  # Home view for the root URL
    path('register/', register_page, name='register'),
    path('login/', login_page, name='login'),
    path('logout/', logout_page, name='logout'),
    path('profile/', profile_page, name='profile'),
    
    path('posts/', PostListView.as_view(), name='post-list'),  # List all posts
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),  # View a single post
    path('posts/new/', PostCreateView.as_view(), name='post-create'),  # Create a new post
    path('posts/<int:pk>/edit/', PostUpdateView.as_view(), name='post-update'),  # Edit an existing post
    path('posts/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),  # Delete a post
]