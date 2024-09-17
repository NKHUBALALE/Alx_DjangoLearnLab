# blog/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Comment  # Import your Post and Comment model 

class CustomUserForm(UserCreationForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    email = forms.EmailField(required=True)

    class Meta:
        """
        The Meta class is used to define the fields to include in the form,
        and their order.
        """
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class PostForm(forms.ModelForm):
    """
    A form that creates or updates a blog post.
    """
    class Meta:
        model = Post
        fields = ['title', 'content']  # Include fields for title and content


class CommentForm(forms.ModelForm):
    """
    A form that creates a comment for a blog post.
    """
    class Meta:
        model = Comment
        fields = ['content']  # Only allow users to enter content for comments
