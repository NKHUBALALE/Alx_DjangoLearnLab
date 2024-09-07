from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Book
from .serializers import BookSerializer

class BookAPITestCase(APITestCase):
    def setUp(self):
        # Create a user for authentication
        self.user = User.objects.create_user(username='testuser', password='testpass')
        
        # Create a book instance for testing
        self.book = Book.objects.create(
            title='Test Book',
            author='Test Author',
            publication_year=2024
        )
        
        # Define the API endpoints
        self.books_url = reverse('book-list')
        self.book_detail_url = reverse('book-detail', kwargs={'pk': self.book.pk})
        self.book_update_url = reverse('book-update', kwargs={'pk': self.book.pk})
        self.book_delete_url = reverse('book-delete', kwargs={'pk': self.book.pk})
    
    def test_list_books(self):
        response = self.client.get(self.books_url)
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
    
    def test_create_book(self):
        # Login the user
        self.client.login(username='testuser', password='testpass')
        data = {
            'title': 'New Book',
            'author': 'New Author',
            'publication_year': 2023
        }
        response = self.client.post(self.books_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)
        self.assertEqual(Book.objects.latest('id').title, 'New Book')
    
    def test_update_book(self):
        # Login the user
        self.client.login(username='testuser', password='testpass')
        data = {
            'title': 'Updated Book',
            'author': 'Updated Author',
            'publication_year': 2025
        }
        response = self.client.put(self.book_update_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Updated Book')
    
    def test_delete_book(self):
        # Login the user
        self.client.login(username='testuser', password='testpass')
        response = self.client.delete(self.book_delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)
    
    def test_filter_books(self):
        response = self.client.get(self.books_url, {'title': 'Test Book'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_search_books(self):
        response = self.client.get(self.books_url, {'search': 'Test Book'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_ordering_books(self):
        Book.objects.create(title='Another Book', author='Another Author', publication_year=2022)
        response = self.client.get(self.books_url, {'ordering': 'publication_year'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        books = response.data
        self.assertTrue(books[0]['publication_year'] <= books[1]['publication_year'])
    
    def test_permission_required_for_create_update_delete(self):
        # No login attempt
        response = self.client.post(self.books_url, {'title': 'Unauthorized Book'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.put(self.book_update_url, {'title': 'Unauthorized Update'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.delete(self.book_delete_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
