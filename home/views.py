from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.models import User
from .forms import ContactForm, ProductForm
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
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            new_product = form.save(commit=False)

            # Fetch selected category OR create a new one
            existing_category = form.cleaned_data.get("existing_category")
            new_category_name = form.cleaned_data.get("new_category")

            if new_category_name:
                category, created = Category.objects.get_or_create(
                    friendly_name=new_category_name
                )
                new_product.category = category
            elif existing_category:
                new_product.category = existing_category

            new_product.save()
            messages.success(request, "New LEGO set added successfully!")

            # Send Email Notification to Admins
            admin_users = User.objects.filter(is_staff=True)
            admin_emails = [
                admin.email for admin in admin_users if admin.email
            ]

            subject = "New Product Added - Brick Heroes"
            context = {'product': new_product}
            email_html_message = render_to_string(
                'allauth/account/product_added_confirmation.html', context
            )
            email_plain_message = strip_tags(email_html_message)

            send_mail(
                subject=subject,
                message=email_plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=admin_emails,
                html_message=email_html_message,
                fail_silently=False,
            )

            return redirect("manage_store")

        else:
            messages.error(request, "Error adding LEGO set. Please check.")

    else:
        form = ProductForm()

    context = {
        "products": products,
        "categories": categories,
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
            if "image" in request.FILES:
                product.image = request.FILES["image"]
            else:
                product.image = product.image  # Retain the existing image
            form.save()
            messages.success(request, "LEGO set updated successfully!")
            return redirect("manage_store")
        else:
            messages.error(request, "Error updating LEGO set.")

    else:
        form = ProductForm(instance=product)

    return render(
        request, "home/edit_product.html", {"form": form, "product": product}
    )


@staff_member_required
def delete_product(request, product_id):
    """Deletes a LEGO set."""
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    messages.success(request, "LEGO set deleted successfully.")
    return redirect("manage_store")


def index(request):
    random_products = list(
        Product.objects.filter(is_borrowed=False).exclude(image="")
    )
    random.shuffle(random_products)
    return render(
        request, 'home/index.html', {'random_products': random_products[:6]}
    )


def custom_404(request, exception):
    return render(request, '404.html', status=404)


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


def subscription_plans(request):
    """Display subscription plans."""
    return render(request, 'products/subscription_plans.html')


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save()

            # Send Confirmation Email to User
            subject = "Thank You for Contacting Us!"
            context = {'user_name': contact_message.name}
            email_html_message = render_to_string(
                'allauth/account/contact_confirmation.html', context
            )
            email_plain_message = strip_tags(email_html_message)

            send_mail(
                subject=subject,
                message=email_plain_message,  # Plain text fallback
                from_email="brickheroes51@gmail.com",
                recipient_list=[contact_message.email],
                html_message=email_html_message,  # HTML email version
                fail_silently=False,
            )

            messages.success(request, "Your message has been sent")
            return redirect('contact_success')

        else:
            messages.error(request, "There was an error with your submission.")
    else:
        form = ContactForm()
    return render(request, "home/index.html", {"form": form})


def contact_success(request):
    return render(request, 'home/contact_success.html')


def privacy_policy(request):
    return render(request, 'home/privacy_policy.html')
