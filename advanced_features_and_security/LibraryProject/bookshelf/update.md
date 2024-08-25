# Update Operation

In this section, we document how the `Book` instance's title was updated in the Django shell.

## Command:

```python
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()

# Expected Output: <Book: Nineteen Eighty-Four>
