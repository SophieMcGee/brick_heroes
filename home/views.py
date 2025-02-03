from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Review, Notification, LegoSet
from .forms import LegoSetForm
from subscriptions.models import Borrowing, Subscription
from notifications.models import Notification
from products.models import Product
import random


def index(request):
    random_products = list(Product.objects.filter(is_borrowed=False))
    random.shuffle(random_products)
    return render(request, 'home/index.html', {'random_products': random_products[:6]})


@login_required
def profile(request):
    return render(request, 'home/profile.html')


def collections(request):
    return render(request, 'home/collections.html')


@login_required
def my_borrowings(request):
    """View for tracking all LEGO sets a user has borrowed."""
    borrowings = (
        Borrowing.objects
        .filter(user=request.user)
        .order_by('-borrowed_on')
    )

    return render(
        request,
        'users/my_borrowings.html',
        {'borrowings': borrowings},
    )


@login_required
def my_reviews(request):
    """ A view to show the user's reviews """
    reviews = Review.objects.filter(user=request.user)
    return render(request, 'home/my_reviews.html', {'reviews': reviews})


@login_required
def my_notifications(request):
    """ A view to show the user's notifications """
    notifications = Notification.objects.filter(
        user=request.user,
        is_read=False,
    )
    return render(
        request,
        'home/my_notifications.html',
        {'notifications': notifications},
    )


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

    return render(
        request,
        'home/edit_legoset.html',
        {
            'form': form,
            'legoset': legoset,
        },
    )


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


@staff_member_required
def admin_notifications(request):
    """Admin-only notifications."""
    admin_notifications = (
        Notification.objects.all()
        .order_by('-created_at')
    )[:10]

    return render(request, 'admin/admin_notifications.html', {
        'admin_notifications': admin_notifications,
    })


@login_required
def user_profile(request):
    """User profile page displaying user info, notifications, borrowed sets."""
    user_profile = get_object_or_404(UserProfile, user=request.user)
    notifications = (
        Notification.objects.filter(user=request.user)
        .order_by('-created_at')
    )[:5]  # Last 5

    borrowed_sets = Borrowing.objects.filter(
        user=request.user,
        is_returned=False,
    )

    return render(request, 'users/user_profile.html', {
        'user_profile': user_profile,
        'notifications': notifications,
        'borrowed_sets': borrowed_sets,
    })


@login_required
def borrow_cart(request):
    """ A view to display items in the borrowing cart """

    # Check if user has a valid subscription
    user_profile = UserProfile.objects.get(user=request.user)
    if not user_profile.subscription:
        messages.error(request, "You need an active subscription to borrow.")
        return redirect('subscription_plans')

    # Retrieve borrowings
    borrowings = Borrowing.objects.filter(user=request.user, is_returned=False)
    total_borrowed = borrowings.count()

    return render(request, 'home/borrow_cart.html', {
        'borrowings': borrowings,
        'total_borrowed': total_borrowed,
    })


def all_products(request):
    """A view to display all Lego sets."""
    return render(request, 'home/all-products.html')


def filter_by_price(request):
    """A view to display Lego sets filtered by price."""
    return render(request, 'home/filter_by_price.html')


def filter_by_rating(request):
    """A view to display Lego sets filtered by rating."""
    return render(request, 'home/filter_by_rating.html')


def filter_by_theme(request):
    """A view to display Lego sets filtered by theme."""
    return render(request, 'home/filter_by_theme.html')


def subscription_plans(request):
    """Display subscription plans."""
    return render(request, 'products/subscription_plans.html')


def gift_cards(request):
    """Display gift card options."""
    return render(request, 'products/gift_cards.html')
