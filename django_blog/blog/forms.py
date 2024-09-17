# blog/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Comment
from taggit.forms import TagField, TagWidget  # Import TagField and TagWidget

class CustomUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class PostForm(forms.ModelForm):
    tags = TagField(required=False, widget=TagWidget())  # Add tags field using TagField and TagWidget

    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']  # Include tags field

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']