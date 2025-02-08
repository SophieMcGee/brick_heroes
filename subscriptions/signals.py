from django.db.models.signals import post_save
from django.dispatch import receiver
from subscriptions.models import Borrowing

@receiver(post_save, sender=Borrowing)
def update_user_profile_with_borrowed_set(sender, instance, created, **kwargs):
    """Update borrowed_this_month when a new borrowing is recorded."""
    if created and not instance.is_returned:
        from subscriptions.models import UserProfile

        user_profile = instance.user.userprofile
        user_profile.borrowed_this_month += 1
        user_profile.save()