from django.db import models
from django.conf import settings
import random
from products.models import Product
from django.utils.timezone import now, timedelta
from notifications.models import Notification
from django.db.models.signals import post_save
from django.dispatch import receiver



class SubscriptionPlan(models.Model):
    """Model for subscription tiers"""
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    max_active_borrows = models.IntegerField()  # Max sets a user can have at once
    can_cancel_anytime = models.BooleanField(default=True)
    stripe_price_id = models.CharField(max_length=255, unique=True, blank=True, null=True)

    def __str__(self):
        return self.name


class Subscription(models.Model):
    """Tracks user subscriptions"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    subscription_plan = models.ForeignKey(
        SubscriptionPlan,
        on_delete=models.CASCADE,
    )
    stripe_subscription_id = models.CharField(max_length=255, null=True, blank=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return (
            f"{self.user.username} - {self.subscription_plan.name} ("
            f"{'Active' if self.status else 'Inactive'})"
        )

    def renew_subscription(self):
        """Extend the subscription for another month"""
        self.start_date = now()
        self.end_date = now() + timedelta(days=30)
        self.status = True
        self.save()

    def cancel_subscription(self):
        """Cancel the subscription and prevent auto-renewal"""
        self.status = False
        self.save()


    def check_expired_subscriptions():
        """Deactivate subscriptions that have passed their end date"""
        expired_subs = Subscription.objects.filter(status=True, end_date__lt=now())
        for sub in expired_subs:
            sub.status = False
            sub.save()


class Borrowing(models.Model):
    """Model for tracking borrowed LEGO sets"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='subscriptions_borrowing'
    )
    subscription = models.ForeignKey(
        'subscriptions.Subscription',  # Use string reference to avoid circular import
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    lego_set = models.ForeignKey(
        'products.Product',  # Reference to Product model
        on_delete=models.SET_NULL,
        null=True,
    )
    borrowed_on = models.DateTimeField(auto_now_add=True)
    returned_on = models.DateTimeField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} borrowed {self.lego_set.name}"


class UserProfile(models.Model):
    """Extended user profile for subscriptions"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    stripe_customer_id = models.CharField(max_length=255, null=True, blank=True)
    subscription = models.ForeignKey(
        "subscriptions.Subscription",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    borrowed_this_month = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

    def can_borrow(self):
        """Check if the user is eligible to borrow on their subscription"""
        if not self.subscription or not self.subscription.status:
            return False
        # Get max sets allowed at the same time
        max_active_borrows = self.subscription.subscription_plan.max_active_borrows

        # Count active borrowed sets
        active_borrows = Borrowing.objects.filter(user=self.user, is_returned=False).count()

        return active_borrows < max_active_borrows

    def get_notifications(self):
        """Fetch the latest notifications for the user"""
        return Notification.objects.filter(user=self.user).order_by('-created_at')[:5]