from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from .models import Book
from django.contrib.auth.decorators import login_required

@login_required
def book_list(request):
    # Check if the user has the required permission
    if not request.user.has_perm('bookshelf.can_view_book'):
        raise PermissionDenied
    
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})
