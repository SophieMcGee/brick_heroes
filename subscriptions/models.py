from django.db import models
from django.conf import settings
import random
from products.models import Product
from django.utils.timezone import now


class SubscriptionPlan(models.Model):
    """Model for subscription tiers"""
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    max_borrow_per_month = models.IntegerField()  # Max sets borrowable
    max_active_borrows = models.IntegerField()  # Max active borrows
    can_cancel_anytime = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
class Subscription(models.Model):
    """Tracks user subscriptions"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subscription_plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True) 
    end_date = models.DateTimeField(null=True, blank=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.subscription_plan.name} ({'Active' if self.status else 'Inactive'})"

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
    lego_set = models.ForeignKey('products.Product', on_delete=models.SET_NULL, null=True)
    borrowed_on = models.DateTimeField(auto_now_add=True)
    returned_on = models.DateTimeField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} borrowed {self.lego_set.name}"


class UserProfile(models.Model):
    """Extended user profile for subscriptions"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subscription = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True)
    borrowed_this_month = models.IntegerField(default=0)  # Tracks monthly borrow count

    def __str__(self):
        return self.user.username

    def can_borrow(self):
        """Check if the user is eligible to borrow based on their subscription"""
        if not self.subscription or not self.subscription.status:
            return False
        active_borrows = Borrowing.objects.filter(user=self.user, is_returned=False).count()
        return active_borrows < self.subscription.subscription_plan.max_active_borrows

    def random_lego_set(self):
        """Get a random LEGO set for the user"""
        available_sets = Product.objects.filter(is_borrowed=False)
        if available_sets.exists():
            return random.choice(available_sets)
        return None
