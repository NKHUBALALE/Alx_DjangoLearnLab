from django.urls import path, include
from .views import BookList
from rest_framework.routers import DefaultRouter
from .views import BookViewSet

# Create a router and register the BookViewSet
router = DefaultRouter()
router.register(r'books', BookViewSet)


urlpatterns = [
    path('books/', BookList.as_view(), name='book-list'),
    path('api/', include(router.urls))
]
