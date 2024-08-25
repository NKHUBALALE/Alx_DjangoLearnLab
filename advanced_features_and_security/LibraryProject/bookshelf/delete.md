# Delete Operation

In this section, we document how the `Book` instance was deleted in the Django shell.

## Command:

```python
from bookshelf.models import Book

# Retrieve and delete the book instance
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()

# Verify deletion
remaining_books = Book.objects.all()
print(remaining_books)  # Expected Output: <QuerySet []> (empty list, confirming deletion)
