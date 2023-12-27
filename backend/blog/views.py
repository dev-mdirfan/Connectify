from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, increment_views, toggle_likes


class PostListView(ListView):
    """
    A view that displays a list of posts.
    """
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-created_at']
    paginate_by = 10

    def get_queryset(self):
        """
        Override the get_queryset method to add filter options.
        """
        queryset = super().get_queryset()

        # Get the filter option from the request
        filter_option = self.request.GET.get('filter_option')

        if filter_option == 'latest':
            # Filter by latest posts
            queryset = queryset.order_by('-updated_at')
        elif filter_option == 'popular_likes':
            # Filter by popular posts based on likes
            queryset = queryset.order_by('-likes')
        elif filter_option == 'popular_views':
            # Filter by popular posts based on views
            queryset = queryset.order_by('-views')
        else:
            # Default queryset
            queryset = queryset.order_by('-created_at')

        return queryset

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
        increment_views(self.kwargs['pk'])
        return super().get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        """
        Handle the POST request for the post detail view.
        If the 'like' parameter is present in the request, toggle the likes count.
        """
        post = self.get_object()

        if request.POST.get('like'):
            # Ensure the user is authenticated before toggling likes
            if request.user.is_authenticated:
                # Toggle the likes count
                updated_likes, liked = toggle_likes(post.pk, request.user)
                if liked:
                    return HttpResponse(f"Post liked. Likes incremented to {updated_likes}")
                else:
                    return HttpResponse(f"Post unliked. Likes decremented to {updated_likes}")
            else:
                return HttpResponse("User must be authenticated to like/unlike a post")

        return super().post(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Retrieve the author's latest six posts
        author_posts = Post.objects.filter(author=self.object.author).exclude(pk=self.object.pk).order_by('-created_at')[:6]

        context['author_posts'] = author_posts
        return context

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


