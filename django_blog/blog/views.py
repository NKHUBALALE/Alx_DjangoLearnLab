# blog/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Post
from .forms import CustomUserForm, PostForm  # Ensure PostForm is imported
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin  # Import UserPassesTestMixin


def home_view(request):
    """
    A view that returns a simple "Welcome to the Blog!" message.

    Args:
        request (HttpRequest): The incoming request.

    Returns:
        HttpResponse: An HTTP response containing the message.
    """

    return HttpResponse("Welcome to the Blog!")

def register_page(request):
    
    """
    A view that handles the registration of new users.

    If the request method is POST, validate the form data and create a new user if
    the form is valid. Log in the user and redirect them to the profile page.

    If the request method is GET, return a registration form.

    Args:
        request (HttpRequest): The incoming request.

    Returns:
        HttpResponse: An HTTP response containing the registration form or redirecting
        the user to the profile page.
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
    A view that handles user login.

    If the request method is POST, authenticate the user and log them in if
    the credentials are valid. Redirect the user to the profile page after
    login.

    If the request method is GET, return a login form.

    Args:
        request (HttpRequest): The incoming request.

    Returns:
        HttpResponse: An HTTP response containing the login form or redirecting
        the user to the profile page.
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
    A view that logs out the user and redirects them to the login page.

    Args:
        request (HttpRequest): The incoming request.

    Returns:
        HttpResponse: An HTTP response redirecting the user to the login page.
    """
    logout(request)
    return redirect('login')  # Redirect to login page after logout

@login_required
def profile_page(request):
    """
    A view that handles the user profile page.

    If the request method is POST, validate the form data and update the user
    if the form is valid. Redirect the user to the profile page after updating
    the user.

    If the request method is GET, return a profile form.

    Args:
        request (HttpRequest): The incoming request.

    Returns:
        HttpResponse: An HTTP response containing the profile form or redirecting
        the user to the profile page.
    """
    if request.method == 'POST':
        form = CustomUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to profile page after saving changes
    else:
        form = CustomUserForm(instance=request.user)
    return render(request, 'blog/profile.html', {'form': form})


class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'  # Create this template

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'  # Create this template

class PostCreateView(LoginRequiredMixin, CreateView):  # Add LoginRequiredMixin here
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'  # Create this template

    def form_valid(self, form):
        form.instance.author = self.request.user  # Set the author to the logged-in user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    A view that allows users to update their own blog posts.

    This view is protected by the `LoginRequiredMixin`, which ensures that only
    logged-in users can access the form. The `UserPassesTestMixin` is used to
    ensure that only the post author can update the post.
    """
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'  # Reuse the same template for creating and updating

    def form_valid(self, form):
        """
        Override the form_valid method to set the author of the post to the
        logged-in user.

        Args:
            form (PostForm): The form containing the post data

        Returns:
            HttpResponse: The response to the form submission
        """
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):  
        """
        Ensure that only the author of the post can update it.

        Returns:
            bool: True if the request user is the author of the post, False otherwise
        """

        post = self.get_object()
        return self.request.user == post.author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    A view that allows users to delete their own blog posts.

    This view is protected by the `LoginRequiredMixin`, which ensures that only
    logged-in users can access the form. The `UserPassesTestMixin` is used to
    ensure that only the post author can delete the post.
    """
    model = Post
    template_name = 'blog/post_confirm_delete.html'  # Create this template
    success_url = reverse_lazy('post-list')  # Redirect to the list view after deletion

    def test_func(self):  # This ensures only the post author can delete the post
        """
        Ensure that only the author of the post can delete it.

        Returns:
            bool: True if the request user is the author of the post, False otherwise
        """
        post = self.get_object()
        return self.request.user == post.author
