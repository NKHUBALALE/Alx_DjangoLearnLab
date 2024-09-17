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
    search_posts,
    PostByTagListView,
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
    path('post/<int:pk>/comments/new/', add_comment, name='add-comment'),  # Add a new comment
    path('comment/<int:pk>/update/', edit_comment, name='comment-update'),  # Update a comment (aligned with format)
    path('comment/<int:pk>/delete/', delete_comment, name='delete-comment'),  # Delete a comment
    # Tagging and Search URLs
    path('search/', search_posts, name='search-posts'),  # Search functionality

    # Tag-based filtering
    path('tags/<slug:tag_slug>/', PostByTagListView.as_view(), name='post-by-tag'),  # View posts by a specific tag
]
