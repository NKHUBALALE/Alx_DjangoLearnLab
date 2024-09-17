# blog/models.py
from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    """
    A blog post model.

    Attributes:
        title (CharField): The title of the post.
        content (TextField): The content of the post.
        published_date (DateTimeField): The date the post was published.
        author (ForeignKey to User): The user who wrote the post.
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Comment(models.Model):
    """
    A comment model.

    Attributes:
        post (ForeignKey to Post): The post the comment is on.
        author (ForeignKey to User): The user who wrote the comment.
        content (TextField): The content of the comment.
        created_at (DateTimeField): The date the comment was created.
        updated_at (DateTimeField): The date the comment was last updated.
    """

    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Return a string representation of the comment.

        The string is formatted as: "Comment by <author> on <post title>"

        :return: A string representation of the comment
        """
        return f'Comment by {self.author.username} on {self.post.title}'
