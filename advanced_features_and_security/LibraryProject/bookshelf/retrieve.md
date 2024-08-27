# Retrieve Operation

In this section, we document how the `Book` instance was retrieved in the Django shell.

## Command:

```python
book = Book.objects.get(title="1984")
print(book.title, book.author, book.publication_year)

# Expected Output: 1984 George Orwell 1949
