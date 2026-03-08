"""Signal handlers for synchronising users and profiles."""

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import UserProfile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a profile automatically whenever a new user is created."""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Ensure the related profile is saved after the user record changes."""
    if hasattr(instance, 'userprofile'):
        instance.userprofile.save()
