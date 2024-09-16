# blog/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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
