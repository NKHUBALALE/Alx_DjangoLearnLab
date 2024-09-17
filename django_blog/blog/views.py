# blog/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Post, Comment  # Ensure Comment model is imported
from .forms import CustomUserForm, PostForm, CommentForm  # Ensure CommentForm is imported
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


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


class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'  # Create this template

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'  # Create this template

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user  # Set the author to the logged-in user
            comment.save()
            return redirect('post-detail', pk=post.id)  # Redirect to the post detail page
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment.html', {'form': form, 'post': post})

@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('post-detail', pk=comment.post.id)  # Redirect to the post detail page
    else:
        form = CommentForm(instance=comment)
    return render(request, 'blog/edit_comment.html', {'form': form})

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST':
        comment.delete()
        return redirect('post-detail', pk=comment.post.id)  # Redirect to the post detail page
    return render(request, 'blog/delete_comment.html', {'comment': comment})

class PostCreateView(LoginRequiredMixin, CreateView):  
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'  

    def form_valid(self, form):
        form.instance.author = self.request.user  
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'  

    def form_valid(self, form):
        form.instance.author = self.request.user  
        return super().form_valid(form)

    def test_func(self):  
        post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'  
    success_url = reverse_lazy('post-list')  

    def test_func(self):  
        post = self.get_object()
        return self.request.user == post.author