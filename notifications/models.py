from django.db import models
from django.contrib.auth.models import User


class Notification(models.Model):
    CATEGORY_CHOICES = [
        ('subscription', 'Subscription'),
        ('borrowing', 'Borrowing'),
        ('review', 'Review'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()
    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, default='subscription'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.category} - {self.message[:50]}"
