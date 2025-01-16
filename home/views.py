from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Borrowing, Review

def index(request):
    """ A view to return the index page """
    return render(request, 'home/index.html')

@login_required
def profile(request):
    return render(request, 'home/profile.html')

def collections(request):
    return render(request, 'home/collections.html')

@login_required
def my_borrowings(request):
    """ A view to show the user's borrowed Lego sets """
    borrowings = Borrowing.objects.filter(user=request.user, is_returned=False)
    return render(request, 'home/my_borrowings.html', {'borrowings': borrowings})

@login_required
def my_reviews(request):
    """ A view to show the user's reviews """
    reviews = Review.objects.filter(user=request.user)
    return render(request, 'home/my_reviews.html', {'reviews': reviews})