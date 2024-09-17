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
    add_comment,
    edit_comment,
    delete_comment,
)   

urlpatterns = [
    path('', home_view, name='home'),  # Home view for the root URL
    path('register/', register_page, name='register'),
    path('login/', login_page, name='login'),
    path('logout/', logout_page, name='logout'),
    path('profile/', profile_page, name='profile'),
    
    path('post/new/', PostCreateView.as_view(), name='post-create'),  # Create a new post
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),  # View a single post
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),  # Update an existing post
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),  # Delete a post

    # Comment URLs
    path('post/<int:pk>/comments/new/', add_comment, name='add-comment'),  # Add a new comment (updated)
    path('comment/<int:pk>/edit/', edit_comment, name='edit-comment'),  # Edit a comment (updated)
    path('comment/<int:pk>/delete/', delete_comment, name='delete-comment'),  # Delete a comment (updated)
]