from django.db import models
from django.conf import settings
from products.models import Product
from django.utils.timezone import now, timedelta
from notifications.models import Notification
from django.db.models.signals import post_save
from django.dispatch import receiver
import stripe


class SubscriptionPlan(models.Model):
    """Model for subscription tiers"""
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    max_active_borrows = models.IntegerField()  # Max sets a user can have
    can_cancel_anytime = models.BooleanField(default=True)
    stripe_price_id = models.CharField(
        max_length=255, unique=True, blank=True, null=True
    )

    def __str__(self):
        return self.name


# Subscription model
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
    stripe_subscription_id = models.CharField(
        max_length=255, null=True, blank=True
    )
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
        """Cancel the subscription in Stripe and update the database"""
        if not self.stripe_subscription_id:
            return  # Avoid breaking if no Stripe ID exists

        try:
            stripe_sub = stripe.Subscription.retrieve(
                self.stripe_subscription_id
            )

            if stripe_sub.status != "canceled":
                stripe.Subscription.modify(
                    self.stripe_subscription_id,
                    cancel_at_period_end=True  # Prevents auto-renewal
                )

                # Mark subscription as canceled in DB
                self.status = False
                self.save()
        except stripe.error.InvalidRequestError as e:
            print(f"ERROR: Stripe cancellation failed - {e}")

    @staticmethod
    def check_expired_subscriptions():
        """Deactivate subscriptions that have passed their end date"""
        expired_subs = Subscription.objects.filter(
            status=True, end_date__lt=now()
        )
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
        'subscriptions.Subscription',  # Always requires an active subscription
        on_delete=models.CASCADE
    )
    lego_set = models.ForeignKey(
        'products.Product',
        on_delete=models.SET_NULL,
        null=True,
    )
    borrowed_on = models.DateTimeField(auto_now_add=True)
    returned_on = models.DateTimeField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} borrowed {self.lego_set.name}"


# User Profile Model
class UserProfile(models.Model):
    """Extended user profile for subscriptions"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    stripe_customer_id = models.CharField(
        max_length=255, null=True, blank=True
    )
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
        """Check if the user is eligible to borrow based on subscription"""
        if not self.subscription:
            return False  # No subscription, cannot borrow

        # Check if active OR pending cancellation but not expired
        if self.subscription.status or (
            self.subscription.end_date and self.subscription.end_date > now()
        ):
            max_active_borrows = (
                self.subscription.subscription_plan.max_active_borrows
            )

            active_borrows = Borrowing.objects.filter(
                user=self.user,
                is_returned=False
            ).count()

            return active_borrows < max_active_borrows

        return False  # Expired subscription, cannot borrow

    def get_notifications(self):
        """Fetch the latest notifications for the user"""
        return Notification.objects.filter(
            user=self.user
        ).order_by('-created_at')[:5]
