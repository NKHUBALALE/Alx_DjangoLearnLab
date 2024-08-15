# Delete Operation

In this section, we document how the `Book` instance was deleted in the Django shell.

## Command:

```python
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()

# Expected Output: (1, {'bookshelf.Book': 1})
