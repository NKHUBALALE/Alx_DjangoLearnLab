from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, FeedView, LikePostView, UnlikePostView

# Router for posts and comments
router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)

# Combined urlpatterns
urlpatterns = [
    path('', include(router.urls)),  # For posts and comments
    path('feed/', FeedView.as_view(), name='user-feed'),  # User feed
    path('<int:pk>/like/', LikePostView.as_view(), name='like-post'),  # Like a post
    path('<int:pk>/unlike/', UnlikePostView.as_view(), name='unlike-post'),  # Unlike a post
]
