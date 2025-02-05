from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from django.apps import apps
from django.db.models import Avg


class Product(models.Model):
    sku = models.CharField(max_length=254, unique=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    difficulty = models.CharField(max_length=50, null=True, blank=True)
    theme = models.CharField(max_length=50, null=True, blank=True)
    is_borrowed = models.BooleanField(default=False)
    stock = models.PositiveIntegerField(default=0)

    @property
    def average_rating(self):
        """Calculates the average rating of a product from all reviews"""
        avg_rating = self.reviews.aggregate(Avg('rating'))['rating__avg']
        return round(avg_rating, 1) if avg_rating else 0

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name

    class Meta:
        verbose_name_plural = "Categories"


class Review(models.Model):
    """Stores reviews for LEGO sets"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name="reviews")
    content = models.TextField()
    rating = models.PositiveIntegerField(default=1)  # Ensure rating is stored
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')  # Users can only review once per product

    def __str__(self):
        return f"Review by {self.user.username} for {self.product.name}"

    def save(self, *args, **kwargs):
        """Update the product's average rating when a new review is saved"""
        super().save(*args, **kwargs)
