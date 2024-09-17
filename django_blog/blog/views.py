from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Post, Comment  # Ensure Comment model is imported
from .forms import CustomUserForm, PostForm, CommentForm  # Ensure CommentForm is imported
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# Blog Post Views
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'  # Create this template

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'  # Create this template

# Add Comment Views
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'  # Create this template

    def form_valid(self, form):
        form.instance.author = self.request.user  # Set the author to the logged-in user
        form.instance.post = get_object_or_404(Post, id=self.kwargs['post_id'])  # Link the comment to the post
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.kwargs['post_id']})  # Redirect to the post detail view

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'  # Reuse the comment form template

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author  # Ensure only the comment author can update it

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.object.post.id})  # Redirect to the post detail view

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'  # Create this template

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author  # Ensure only the comment author can delete it

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.object.post.id})  # Redirect to the post detail view

# Blog Post Views (Unchanged)
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
