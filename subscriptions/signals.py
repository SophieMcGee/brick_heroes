from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Subscription, UserProfile

@receiver(post_save, sender=Subscription)
def update_user_profile_with_subscription(sender, instance, created, **kwargs):
    """Automatically update the UserProfile with the active subscription when a new subscription is created."""
    if created:
        user_profile = instance.user.userprofile
        user_profile.subscription = instance
        user_profile.save()