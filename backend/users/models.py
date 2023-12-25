from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image


def profile_image_dir(instance, filename):
    """
    Returns the path to the profile image.
    """
    username = instance.user.username
    extension = filename.split('.')[-1]
    new_filename = f'{username}_profile.{extension}'
    return f'profile_images/{username}/{new_filename}'


def profile_background_dir(instance, filename):
    """
    Returns the path to the profile background image.
    """
    username = instance.user.username
    extension = filename.split('.')[-1]
    new_filename = f'{username}_background.{extension}'
    return f'profile_backgrounds/{username}/{new_filename}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=100, default='Connectify - Where Connections Unite!', blank=True)
    location = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_image = models.ImageField(
        upload_to=profile_image_dir, default='profile_images/default_profile.jpg', blank=True)
    profile_background = models.ImageField(
        upload_to=profile_background_dir, default='profile_backgrounds/default_background.jpg', blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def get_absolute_url(self):
        """
        Returns the absolute URL of the profile.
        """
        return reverse('profile', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        """
        Overriding the save method to delete the old profile image/background when a new one is uploaded
        and reduce the size of the image.
        """
        try:
            this = Profile.objects.get(id=self.id)
            if this.profile_image != self.profile_image:
                this.profile_image.delete(save=False)
            if this.profile_background != self.profile_background:
                this.profile_background.delete(save=False)
        except:
            pass

        super().save(*args, **kwargs)

        if self.profile_image:
            img = Image.open(self.profile_image.path)
            max_size = (300, 300)  # Set the maximum size for the image
            img.thumbnail(max_size)
            img.save(self.profile_image.path)

        if self.profile_background:
            bg_img = Image.open(self.profile_background.path)
            # Process the background image as needed
            bg_img.save(self.profile_background.path)



