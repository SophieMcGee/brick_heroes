from django.db import models
from django.contrib.auth.models import User


class LegoSet(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    piece_count = models.IntegerField()
    image = models.ImageField(upload_to='legosets/')
    availability = models.BooleanField(default=True)
    theme = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} ({self.email})"


class Borrowing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lego_set = models.CharField(max_length=255)
    due_date = models.DateField()
    is_returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.lego_set} (Due: {self.due_date})"
