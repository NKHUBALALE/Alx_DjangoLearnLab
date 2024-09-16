# blog/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserForm

def register_page(request):
    """
    Handles user registration.

    If the request method is POST, it creates a new user using the submitted form data.
    If the form is valid, it logs in the user and redirects them to the profile page.
    If the request method is GET, or if the form is invalid, it renders the registration form template.
    """
    
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in the user after registration
            return redirect('profile')  # Redirect to profile page after registration
    else:
        form = CustomUserForm()
    return render(request, 'blog/register.html', {'form': form})

def login_page(request):
    """
    Handles user login.

    If the request method is POST, it authenticates the user using the submitted form data.
    If the user is valid, it logs in the user and redirects them to the profile page.
    If the request method is GET, or if the user is invalid, it renders the login form template.
    """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')  # Redirect to profile page after login
    return render(request, 'blog/login.html')

def logout_page(request):
    """
    Handles user logout.

    Logs out the user and redirects them to the login page.
    """
    logout(request)
    return redirect('login')  # Redirect to login page after logout

@login_required
def profile_page(request):
    """
    Handles user profile page.

    If the request method is POST, it updates the user's information using the submitted form data.
    If the form is valid, it saves the changes and redirects the user to the profile page.
    If the request method is GET, or if the form is invalid, it renders the profile page template with the user's information.
    """
    if request.method == 'POST':
        form = CustomUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to profile page after saving changes
    else:
        form = CustomUserForm(instance=request.user)
    return render(request, 'blog/profile.html', {'form': form})