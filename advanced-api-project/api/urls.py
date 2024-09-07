from django.urls import path
from .views import BookListView, BookDetailView

urlpatterns = [
    path('books/', BookListView.as_view(), name='book-list'),  # List all books or create a new one
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),  # Retrieve, update, or delete a single book by ID
]
