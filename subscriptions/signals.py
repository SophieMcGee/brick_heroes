from django.db.models.signals import post_save
from django.dispatch import receiver
from subscriptions.models import Borrowing
from django.contrib.auth.models import User
from .models import UserProfile

@receiver(post_save, sender=Borrowing)
def update_user_profile_with_borrowed_set(sender, instance, created, **kwargs):
    """Update borrowed_this_month when a new borrowing is recorded."""
    if created and not instance.is_returned:
        from subscriptions.models import UserProfile

        user_profile = instance.user.userprofile
        user_profile.borrowed_this_month += 1
        user_profile.save()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()