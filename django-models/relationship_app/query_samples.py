import django
from django.conf import settings
from relationship_app.models import Author, Book, Library, Librarian

# Ensure Django settings are configured
django.setup()

def query_all_books_by_author(author_name):
    try:
        author = Author.objects.get(name=author_name)
        # Use filter to get books by a specific author
        books = Book.objects.filter(author=author)
        return books
    except Author.DoesNotExist:
        return f"No author found with name {author_name}"

def list_all_books_in_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()
        return books
    except Library.DoesNotExist:
        return f"No library found with name {library_name}"

def retrieve_librarian_for_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        # Retrieve the librarian using the library instance
        librarian = Librarian.objects.get(library=library)
        return librarian
    except Library.DoesNotExist:
        return f"No library found with name {library_name}"
    except Librarian.DoesNotExist:
        return f"No librarian found for library {library_name}"

# Sample usage:
if __name__ == "__main__":
    print("Books by Author 'John Doe':", query_all_books_by_author('John Doe'))
    print("Books in Library 'Central Library':", list_all_books_in_library('Central Library'))
    print("Librarian for Library 'Central Library':", retrieve_librarian_for_library('Central Library'))
