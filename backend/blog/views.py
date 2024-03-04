from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Like, increment_views, toggle_likes, get_like_status, get_like_users
from django.contrib import messages
from .forms import PostForm


class PostListView(ListView):
    """
    A view that displays a list of posts.
    """
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-created_at']
    paginate_by = 5

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
                    # Message on successful like
                    messages.success(request, f'You liked this post!')
                    return redirect('post-detail', pk=post.pk)
                else:
                    # Message on successful unlike
                    messages.success(request, f'You unliked this post!')
                    return redirect('post-detail', pk=post.pk)
            else:
                # Message on unsuccessful like
                messages.error(
                    request, f'You must be logged in to like/unlike a post!')
                return redirect('post-detail', pk=post.pk)

        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Add additional context data to the template.
        - Retrieve the author's latest six posts.
        - Add the 'like_status' to the context.
        """
        context = super().get_context_data(**kwargs)

        # Retrieve the author's latest six posts
        author_posts = Post.objects.filter(author=self.object.author).exclude(
            pk=self.object.pk).order_by('-created_at')[:6]
        # Add 'author_posts' to the context
        context['author_posts'] = author_posts

        # Get the post object
        post = self.get_object()
        # Get the like status for the current user
        like_status = get_like_status(post.pk, self.request.user)
        # Add 'like_status' to the context
        context['like_status'] = like_status

        # Get the like users for the post
        like_users = get_like_users(post.pk)
        # Add 'like_users' to the context
        context['like_users'] = like_users

        return context


'''
class LikeView(View):
    model = Like
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
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('blog')
    # fields = ['title', 'description', 'content', 'thumbnail', 'status']

    def form_valid(self, form):
        """
        Set the author of the post as the current user.
        """
        form.instance.author = self.request.user
        # Check for form errors
        if form.is_valid():
            return super().form_valid(form)
        else:
            print(form.errors)
            return self.form_invalid(form)

        # return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    A view for updating an existing post.
    """
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    # fields = ['title', 'content', 'thumbnail']
    # success_url should return to where the user came from
    success_url = reverse_lazy('post-detail')

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
    # Replace with your actual template name
    template_name = 'blog/post_confirm_delete.html'
    # Replace 'post-list' with your actual URL name
    success_url = reverse_lazy('post-list')

    def test_func(self):
        """
        Check if the current user is the author of the post.
        """
        post = self.get_object()
        return self.request.user == post.author
