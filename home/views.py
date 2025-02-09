from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .forms import ContactForm
from subscriptions.models import Borrowing, Subscription, UserProfile
from notifications.models import Notification
from products.models import Product, Review, Category
from allauth.account.models import EmailAddress
from cart.models import BorrowOrder
import random
from django.conf import settings
from home.forms import ProductForm
import stripe


stripe.api_key = settings.STRIPE_SECRET_KEY

@staff_member_required
def manage_store(request):
    """View to manage LEGO sets, subscribers, and borrowing."""
    products = Product.objects.all()
    categories = Category.objects.all()
    subscriptions = Subscription.objects.filter(status=True)
    borrowed_sets = BorrowOrder.objects.filter(status="Pending")  # Active borrowings
    returned_sets = BorrowOrder.objects.filter(status="Returned")  # Returned sets

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)  # Include FILES to handle image upload
        if form.is_valid():
            new_product = form.save(commit=False)  # Don't save yet, modify first

            category_name = request.POST.get("theme")  # Get selected category from form
            if category_name:
                category, created = Category.objects.get_or_create(friendly_name=category_name)
                new_product.category = category  # Assign category to product

            # Handle image upload
            if "image" in request.FILES:
                new_product.image = request.FILES["image"]
            elif new_product.image:
                pass  # Keep existing image if no new image is uploaded

            new_product.save()  # Save the new product

            return redirect("manage_store")

    else:
        form = ProductForm()

    context = {
        "products": products,
        "categories": categories,  # Send categories to template
        "subscriptions": subscriptions,
        "borrowed_sets": borrowed_sets,
        "returned_sets": returned_sets,
        "form": form,
    }
    return render(request, "home/manage_store.html", context)


@staff_member_required
def edit_product(request, product_id):
    """Edit an existing LEGO set"""
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "LEGO set updated successfully!")
            return redirect("manage_store")
        else:
            messages.error(request, "Error updating LEGO set.")

    else:
        form = ProductForm(instance=product)

    return render(request, "home/edit_product.html", {"form": form, "product": product})

@staff_member_required
def delete_product(request, product_id):
    """Deletes a LEGO set."""
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    messages.success(request, "LEGO set deleted successfully.")
    return redirect("manage_store")

@staff_member_required
def cancel_subscription(request, subscription_id):
    """Cancels a user's subscription and removes it from Stripe."""
    subscription = get_object_or_404(Subscription, id=subscription_id)

    try:
        stripe.Subscription.delete(subscription.stripe_subscription_id)
        subscription.status = False
        subscription.save()
        messages.success(request, "Subscription cancelled successfully.")
    except stripe.error.StripeError as e:
        messages.error(request, f" Stripe Error: {str(e)}")

    return redirect("manage_store")

def index(request):
    random_products = list(Product.objects.filter(is_borrowed=False).exclude(image=""))
    random.shuffle(random_products)
    return render(request, 'home/index.html', {'random_products': random_products[:6]})


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


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save()

            # Send an automatic reply to the user
            send_mail(
                subject="Thank You for Contacting Us!",
                message=f"Hello {contact_message.name},\n\n"
                        "Thank you for reaching out! This website is part of a test project for a learning program, messages are not monitored and you will not receive a reply.\n\n"
                        "Best Regards,\nBrick Heroes Team",
                from_email="brickheroes51@gmail",
                recipient_list=[contact_message.email],
                fail_silently=False,
            )

            return redirect('contact_success')
    else:
        form = ContactForm()


def contact_success(request):
    return render(request, 'home/contact_success.html')
