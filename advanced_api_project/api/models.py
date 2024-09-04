from django.db import models

"""
    The Author model represents a writer of one or more books.
    Each author has a name and can be linked to multiple books.
"""
    
class Author(models.Model):
    """
    The Author model represents a writer of one or more books.
    Each author has a name and can be linked to multiple books.
    """


    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Book(models.Model):
    """
    BookSerializer is used to serialize and validate Book instances.
    It ensures that the publication year is not in the future.
    """
     
    title = models.CharField(max_length=200)
    publication_year = models.PositiveIntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')

    def __str__(self):
        return self.title
