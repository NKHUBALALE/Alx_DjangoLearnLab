from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    """
    A blog post model

    Fields:
        title (CharField): The title of the post
        content (TextField): The content of the post
        published_date (DateTimeField): The date the post was published
        author (ForeignKey to User): The user who wrote the post
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        
        """
        Return a string representation of the Post instance
        """
        
        return self.title
