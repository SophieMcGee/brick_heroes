from django.db import models
from django.conf import settings
from products.models import Product
from subscriptions.models import SubscriptionPlan

class Cart(models.Model):
    """Model for user shopping cart"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.username}"

class CartItem(models.Model):
    """Model for Lego sets added to the cart within subscription limits"""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)  # Borrowed Lego sets
    subscription = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE, null=True, blank=True)  # User's subscription plan
    quantity = models.PositiveIntegerField(default=1)  # Number of sets user wants to borrow

    def __str__(self):
        if self.product:
            return f"{self.quantity} x {self.product.name}"
        elif self.subscription:
            return f"Subscription: {self.subscription.name}"
        return "Invalid Cart Item"