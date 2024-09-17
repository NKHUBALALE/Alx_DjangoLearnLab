# blog/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Post
from .forms import CustomUserForm, PostForm  # Ensure PostForm is imported
from django.contrib.auth.mixins import LoginRequiredMixin  # Import LoginRequiredMixin

def home_view(request):
    return HttpResponse("Welcome to the Blog!")

def register_page(request):
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
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')  # Redirect to profile page after login
    return render(request, 'blog/login.html')

def logout_page(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout

@login_required
def profile_page(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to profile page after saving changes
    else:
        form = CustomUserForm(instance=request.user)
    return render(request, 'blog/profile.html', {'form': form})

# Blog Post Views
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

class PostUpdateView(LoginRequiredMixin, UpdateView):  # Add LoginRequiredMixin here
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'  # Reuse the same template for creating and updating

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)  # Only allow authors to edit their posts

class PostDeleteView(LoginRequiredMixin, DeleteView):  # Add LoginRequiredMixin here
    model = Post
    template_name = 'blog/post_confirm_delete.html'  # Create this template
    success_url = reverse_lazy('post-list')  # Redirect to the list view after deletion

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)  # Only allow authors to delete their posts