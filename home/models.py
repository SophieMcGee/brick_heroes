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

class Borrowing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    lego_set = models.ForeignKey(LegoSet, on_delete=models.CASCADE)
    borrow_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    is_returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.lego_set.title}"

from django.db import models
from django.contrib.auth.models import User

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lego_set = models.ForeignKey('LegoSet', on_delete=models.CASCADE)
    review_text = models.TextField()
    rating = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.lego_set.title}"