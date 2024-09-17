from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Post, Comment  # Ensure Comment model is imported
from .forms import CustomUserForm, PostForm, CommentForm  # Ensure CommentForm is imported
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# blog/views.py
from django.shortcuts import render
from django.db.models import Q
from .models import Post

def search_posts(request):
    """
    View to search posts based on title, content, and tags.

    If the query is not empty, it will filter posts based on the query.
    The results will be rendered in the 'blog/search_results.html' template.

    :param request: The request object
    :return: A rendered template with the query results
    """
    
    
    query = request.GET.get('q')  # Get the search query from the request
    results = Post.objects.filter(
        Q(title__icontains=query) | 
        Q(content__icontains=query) | 
        Q(tags__name__icontains=query)
    ).distinct()  # Filter posts based on the query
    return render(request, 'blog/search_results.html', {'results': results, 'query': query})

# Home view
def home_view(request):
    return HttpResponse("Welcome to the Blog!")

# User registration
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

# User login
def login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')  # Redirect to profile page after login
    return render(request, 'blog/login.html')

# User logout
def logout_page(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout

# User profile
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
    template_name = 'blog/post_list.html'

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

# Add Comment Views (Function-Based)
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

# Blog Post Views (Class-Based)
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

# Add Comment Views (Class-Based)
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, id=self.kwargs['post_id'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.kwargs['post_id']})

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.object.post.id})

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.object.post.id})
