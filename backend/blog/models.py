from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.core.files.storage import default_storage
from PIL import Image
import readtime
from django.db import models, transaction
from django.db.models import F


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


def thumbnail_dir(instance, filename):
    """
    Returns the path to the thumbnail image.
    """
    username = instance.author.username
    post_title = instance.title
    extension = filename.split('.')[-1]
    new_filename = f'{post_title}_thumbnail.{extension}'
    return f'posts/thumbnails/{username}/{new_filename}'

class Post(models.Model):
    """
    Represents a blog post in the Connectify application.
    
    It fails to case:
    - thumbnail path does not have post_id
    - image cropping does not work
    """

    # Choices for the status of the post
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )


    # Fields of the Post model
    title = models.CharField(max_length=255)
    content = models.TextField()
    thumbnail = models.ImageField(upload_to=thumbnail_dir, default='posts/thumbnails/default_thumbnail.jpg', blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=255, unique=True, editable=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='published')
    views = models.PositiveIntegerField(default=0, editable=False)
    likes = models.PositiveIntegerField(default=0, editable=False)

    def save(self, *args, **kwargs):
        """
        Override the save method to generate a unique slug and modify the thumbnail size.
        """
        if not self.slug:
            self.slug = slugify(self.title)

        # Check if the thumbnail has been modified
        if self.pk:
            old_post = Post.objects.get(pk=self.pk)
            if self.thumbnail != old_post.thumbnail:
                # Check if the thumbnail file actually exists
                if default_storage.exists(self.thumbnail.name):
                    # Open the uploaded image
                    img = Image.open(self.thumbnail.path)
                    width, height = img.size

                    # Calculate the target aspect ratio (3:2)
                    target_ratio = 3 / 2

                    # Calculate the current aspect ratio
                    current_ratio = width / height

                    if current_ratio > target_ratio:
                        # Crop the width to achieve a 3:2 aspect ratio
                        new_width = int(height * target_ratio)
                        left = (width - new_width) // 2
                        right = left + new_width
                        top = 0
                        bottom = height
                        img = img.crop((left, top, right, bottom))
                    elif current_ratio < target_ratio:
                        # Crop the height to achieve a 3:2 aspect ratio
                        new_height = int(width / target_ratio)
                        top = (height - new_height) // 2
                        bottom = top + new_height
                        left = 0
                        right = width
                        img = img.crop((left, top, right, bottom))

                    # Resize the image to a maximum of 300x300
                    img.thumbnail((300, 300))

                    # Save the modified image
                    img.save(self.thumbnail.path)

        super().save(*args, **kwargs)
    
    def __str__(self):
        """
        Returns a string representation of the Post object.
        
        :return: The title of the post.
        :rtype: str
        """
        return self.title

    class Meta:
        """
        Meta class for the Post model.
        """
        ordering = ['-created_at']
    
    def get_absolute_url(self):
        """
        Returns the absolute URL for the blog post.
        
        :return: The absolute URL for the blog post.
        :rtype: str
        """
        return reverse('post-detail', kwargs={'pk': self.pk})
    
    def get_readtime(self):
        """
        Returns the read time of the post.
        """
        result = readtime.of_text(self.content)
        return result.text 

@transaction.atomic
def increment_counter(pk):
    # Use select_for_update to lock the row during the transaction
    post = Post.objects.select_for_update().get_or_create(pk=pk)[0]

    # Increment the views count directly in the database
    Post.objects.filter(pk=pk).update(views=F('views') + 1)

    # Retrieve the updated value
    updated_value = post.views

    return updated_value


@transaction.atomic
def increment_likes(post_id, user):
    # Use select_for_update to lock the row during the transaction
    post = Post.objects.select_for_update().get_or_create(pk=post_id)[0]

    # Increment the likes count directly in the database
    Post.objects.filter(pk=post_id).update(likes=F('likes') + 1)

    # Create a new Like instance to associate the user with the post
    Like.objects.create(user=user, post=post)

    # Retrieve the updated value
    updated_value = post.likes

    return updated_value