from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

# Signal receiver function that gets triggered after a User object is saved
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """
    Signal receiver function to create a Profile object when a User object is created.
    """
    if created:
        Profile.objects.create(user=instance)

# Signal receiver function that gets triggered after a User object is saved
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    """
    Signal receiver function to save the Profile object when a User object is saved.
    """
    instance.profile.save()
