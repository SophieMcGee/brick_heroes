from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Review, Notification, LegoSet
from .forms import LegoSetForm
from subscriptions.models import Borrowing

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

@login_required
def my_notifications(request):
    """ A view to show the user's notifications """
    notifications = Notification.objects.filter(user=request.user, is_read=False)
    return render(request, 'home/my_notifications.html', {'notifications': notifications})

@staff_member_required
def manage_legosets(request):
    """ A view for superusers to manage Lego sets """
    legosets = LegoSet.objects.all()
    return render(request, 'home/manage_legosets.html', {'legosets': legosets})

@staff_member_required
def edit_legoset(request, legoset_id):
    """ A view to edit a Lego set """
    legoset = get_object_or_404(LegoSet, id=legoset_id)

    if request.method == 'POST':
        form = LegoSetForm(request.POST, request.FILES, instance=legoset)
        if form.is_valid():
            form.save()
            return redirect('manage_legosets')
    else:
        form = LegoSetForm(instance=legoset)

    return render(request, 'home/edit_legoset.html', {'form': form, 'legoset': legoset})

@staff_member_required
def delete_legoset(request, legoset_id):
    """ A view to delete a Lego set """
    legoset = get_object_or_404(LegoSet, id=legoset_id)
    legoset.delete()
    return redirect('manage_legosets')

@staff_member_required
def admin_tools(request):
    """ A view for superusers to access admin tools """
    return render(request, 'home/admin_tools.html')

@login_required
def borrow_cart(request):
    """ A view to display items in the borrowing cart """
    borrowings = Borrowing.objects.filter(user=request.user, is_returned=False)
    total_borrowed = borrowings.count()
    return render(request, 'home/borrow_cart.html', {
        'borrowings': borrowings,
        'total_borrowed': total_borrowed,
    })

def all_products(request):
    """A view to display all Lego sets."""
    return render(request, 'home/all_products.html')

def filter_by_price(request):
    """A view to display Lego sets filtered by price."""
    return render(request, 'home/filter_by_price.html')

def filter_by_rating(request):
    """A view to display Lego sets filtered by rating."""
    return render(request, 'home/filter_by_rating.html')

def filter_by_theme(request):
    """A view to display Lego sets filtered by theme."""
    return render(request, 'home/filter_by_theme.html')