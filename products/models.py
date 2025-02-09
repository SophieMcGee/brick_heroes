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
    total_ratings = models.PositiveIntegerField(default=0)
    average_rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)

    def update_rating(self):
        """Updates the average rating based on user ratings."""
        avg_rating = self.ratings.aggregate(Avg("rating"))["rating__avg"]
        self.average_rating = round(avg_rating, 1) if avg_rating else 0
        self.total_ratings = self.ratings.count()
        self.save()

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
        
class Rating(models.Model):
    """Stores individual ratings for a product."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="ratings")
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])  # 1 to 5 stars
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rating: {self.rating} for {self.product.name}"


class Review(models.Model):
    """Stores written reviews for LEGO sets (requires approval)."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    content = models.TextField()
    rating = models.PositiveIntegerField(default=1)
    created_on = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)  # Needs admin approval

    def __str__(self):
        return f"Review by {self.user.username} for {self.product.name}"
