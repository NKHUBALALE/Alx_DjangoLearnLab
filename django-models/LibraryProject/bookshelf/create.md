# Create Operation

In this section, we document how the book instance was created.

## Command:
```python
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
print(book)
