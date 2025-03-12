from django.db import models
from django.conf import settings
from products.models import Product
from django.utils.timezone import now


class Cart(models.Model):
    """
    Represents a user's borrowing cart.

    Each user can have only one cart, which stores borrowed LEGO sets 
    before confirming the borrow order.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cart",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.username}"


class CartItem(models.Model):
    """Model for tracking borrowed LEGO sets"""
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name="items"
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=1)
    added_on = models.DateTimeField(default=now, editable=False)

    def __str__(self):
        return f"{self.product.name} (Borrowed by {self.cart.user.username})"


class BorrowOrder(models.Model):
    """Model to track each borrow order with delivery info."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    full_name = models.CharField(max_length=100)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default="Pending")

    # Many-to-many relationship with borrowed LEGO sets
    items = models.ManyToManyField(Product, through='BorrowOrderItem')

    def __str__(self):
        return f"Order {self.id} for {self.user.username}"


class BorrowOrderItem(models.Model):
    """Intermediate model to connect BorrowOrder and Product."""
    order = models.ForeignKey(BorrowOrder, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity}x {self.product.name} (Order {self.order.id})"
