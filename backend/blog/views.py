from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, increment_counter, increment_likes


class PostListView(ListView):
    """
    A view that displays a list of posts.
    """
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-created_at']
    paginate_by = 10

class PostDetailView(DetailView):
    """
    A view that displays the details of a post.
    """
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    
    def get(self, request, *args, **kwargs):
        """
        Increment the view count when the detail view is visited.
        """
        # Increment the view count when the detail view is visited
        increment_counter(self.kwargs['pk'])
        return super().get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        """
        Handle the POST request for the post detail view.
        If the 'like' parameter is present in the request, increment the likes count.
        """
        post = self.get_object()

        if request.POST.get('like'):
            # Ensure the user is authenticated before incrementing likes
            if request.user.is_authenticated:
                # Increment the likes count for the post
                updated_likes = increment_likes(post.pk, request.user)
                return HttpResponse(f"Likes incremented to {updated_likes}")
            else:
                return HttpResponse("User must be authenticated to like a post")

        return super().post(request, *args, **kwargs)

'''
class LikeView(View):
    """
    A simple view for incrementing the likes count of a post.
    """
    def post(self, request, *args, **kwargs):
        """
        Handle the POST request for incrementing the likes count.
        """
        post_id = kwargs.get('pk')
        if post_id:
            # Increment the likes count for the post
            updated_likes = increment_likes(post_id)
            # You can use the updated_likes value in your response or redirect logic
            return HttpResponse(f"Likes incremented to {updated_likes}")
        else:
            return HttpResponse("Invalid request")
'''


class PostCreateView(LoginRequiredMixin, CreateView):
    """
    A view for creating a new post.
    """
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content', 'thumbnail']

    def form_valid(self, form):
        """
        Set the author of the post as the current user.
        """
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    A view for updating an existing post.
    """
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content', 'thumbnail']

    def form_valid(self, form):
        """
        Set the author of the post as the current user.
        """
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        """
        Check if the current user is the author of the post.
        """
        post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    A view for deleting a post.
    """
    model = Post
    template_name = 'blog/post_confirm_delete.html'  # Replace with your actual template name
    success_url = reverse_lazy('post-list')  # Replace 'post-list' with your actual URL name

    def test_func(self):
        """
        Check if the current user is the author of the post.
        """
        post = self.get_object()
        return self.request.user == post.author


