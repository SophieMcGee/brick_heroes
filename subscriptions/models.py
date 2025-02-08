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
    max_borrow_per_month = models.IntegerField()
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

    @classmethod
    def borrow_mystery_set(cls, user, subscription):
        """Method to handle borrowing a mystery set."""
        # Ensure the user is on the 'Mystery Subscription'
        if subscription.subscription_plan.name != "Mystery Subscription":
            return None  # Not allowed to borrow a mystery set if not on the Mystery Subscription

        # Ensure the user hasn't already requested a mystery set this month
        if cls.objects.filter(user=user, borrowed_on__month=now().month, lego_set__category__name="Mystery").exists():
            return None  # Already borrowed a mystery set this month

        # Randomly pick an available LEGO set from non-borrowed products
        mystery_set = Product.objects.filter(is_borrowed=False, category__name="Mystery").order_by('?').first()
        if mystery_set:
            # Delay importing the Subscription model to avoid circular import
            from subscriptions.models import Subscription  # Import inside the method

            return cls.objects.create(
                user=user,
                subscription=subscription,
                lego_set=mystery_set,
                is_returned=False
            )
        return None  # No available mystery sets



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
        active_borrows = (
            Borrowing.objects
            .filter(
                user=self.user,
                is_returned=False
            )
            .count()
        )
        return (
            active_borrows < self.subscription.subscription_plan.max_active_borrows
        )

    def reset_monthly_borrow_count(self):
        """Reset the borrow count at the start of each month"""
        self.borrowed_this_month = 0
        self.save()

    def get_notifications(self):
        """Fetch the latest notifications for the user"""
        return Notification.objects.filter(user=self.user).order_by('-created_at')[:5]

    def random_lego_set(self):
        """Get a random LEGO set for the user"""
        available_sets = Product.objects.filter(is_borrowed=False)
        if available_sets.exists():
            return random.choice(available_sets)
        return None

    def has_requested_mystery_set(self):
        """Check if the user has already requested a mystery set this month."""
        return Borrowing.objects.filter(
            user=self.user,
            lego_set__category__name="Mystery",
            borrowed_on__month=now().month
        ).exists()

@receiver(post_save, sender='subscriptions.Borrowing')
def update_user_profile_with_borrowed_set(sender, instance, created, **kwargs):
    """Update borrowed_this_month when a new borrowing is recorded."""
    if created and not instance.is_returned:
        from subscriptions.models import UserProfile

        user_profile = instance.user.userprofile
        user_profile.borrowed_this_month += 1
        user_profile.save()