from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from django.apps import apps
from django.db.models import Avg


class Product(models.Model):
    sku = models.CharField(max_length=254, unique=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    rating = models.FloatField(default=0)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(upload_to="product_images/", blank=True, null=True)
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    difficulty = models.CharField(max_length=50, null=True, blank=True)
    theme = models.CharField(max_length=50, null=True, blank=True)
    is_borrowed = models.BooleanField(default=False)
    stock = models.PositiveIntegerField(default=0)
    total_ratings = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        """Ensure image_url is set correctly on save."""
        if self.image:  # If an image is uploaded
            if "cloudinary" in str(self.image):
                self.image_url = str(self.image)  # Full Cloudinary URL
            else:
                self.image_url = f"/media/{self.image}"  # Local path for static media
        super().save(*args, **kwargs)

    def get_average_rating(self):
        """Calculate the average rating from all reviews."""
        avg_rating = self.reviews.aggregate(Avg('rating'))['rating__avg']
        return round(avg_rating, 1) if avg_rating else 0

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
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="ratings"
    )
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rating for {self.product.name}: {self.rating}/5"


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
