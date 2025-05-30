from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cart, CartItem
from products.models import Product
from subscriptions.models import Borrowing
from notifications.models import Notification
from .forms import DeliveryInfoForm
from django.db import transaction
from django.utils.timezone import now
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


@login_required
def view_cart(request):
    """View for displaying the cart."""
    cart, _ = Cart.objects.get_or_create(user=request.user)

    user_profile = request.user.userprofile
    subscription = user_profile.subscription

    max_active_borrows = 0  # Default if no subscription
    if subscription and subscription.subscription_plan:
        max_active_borrows = subscription.subscription_plan.max_active_borrows

    context = {
        'cart': cart,
        'has_subscribed_items': cart.items.exists(),
        'max_active_borrows': max_active_borrows,  # Pass to template
    }

    return render(request, "cart/shopping_cart.html", context)


@login_required
def process_checkout(request):
    """Stores delivery details and redirects to Stripe Checkout"""
    if request.method == "POST":
        request.session['checkout_details'] = {
            'full_name': request.POST.get('full_name'),
            'address_line1': request.POST.get('address_line1'),
            'address_line2': request.POST.get('address_line2'),
            'city': request.POST.get('city'),
            'postal_code': request.POST.get('postal_code'),
            'country': request.POST.get('country'),
        }

        # Redirect to Stripe Checkout
        return redirect('subscription_checkout')
    return redirect('shopping_cart')


@login_required
def add_to_cart(request, product_id):
    """Add a LEGO set to the cart for borrowing instead of confirm."""
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Ensure user has an active subscription
    subscription = request.user.userprofile.subscription
    if not subscription or not subscription.status:
        messages.error(request, "You need an active subscription to borrow.")
        return redirect("subscription_plans")

    # Get subscription borrowing limit
    max_active_borrows = subscription.subscription_plan.max_active_borrows

    # Count active borrowed sets
    active_borrows = Borrowing.objects.filter(
        user=request.user, is_returned=False
    ).count()

    # Check if borrowing limit is reached
    if active_borrows >= max_active_borrows:
        messages.error(
            request,
            f"You have reached your limit of {max_active_borrows} sets. "
            "Return a set to borrow a new one."
        )
        return redirect("shopping_cart")

    # **Add item to cart instead of confirming the borrow immediately**
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart, product=product
    )

    # Show success message & redirect to the cart page
    messages.success(request, f"{product.name} has been added to your cart!")
    return redirect("shopping_cart")  # Redirects to cart instead of confirming


@login_required
def remove_from_cart(request, item_id):
    """Remove a borrowed LEGO set from the cart."""
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, id=item_id)

    try:
        cart_item.delete()
        messages.success(
            request, f"{cart_item.product.name} has been removed."
        )
    except Exception as e:
        messages.error(request, f"Error removing item: {str(e)}")

    return redirect("shopping_cart")


@login_required
def checkout(request):
    """Handle the checkout process for borrowing LEGO sets."""
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = cart.items.all()

    if not cart_items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect("shopping_cart")

    user_profile = request.user.userprofile
    subscription = user_profile.subscription

    max_active_borrows = (
        subscription.subscription_plan.max_active_borrows
        if subscription else 0
    )

    active_borrows = Borrowing.objects.filter(
        user=request.user, is_returned=False
    ).count()

    # Check if the total would exceed the subscription limit
    if active_borrows + cart_items.count() > max_active_borrows:
        messages.error(
            request,
            f"You can only borrow up to {max_active_borrows} sets at a time. "
            "Please return some sets before borrowing more."
        )
        return redirect("shopping_cart")

    if request.method == "POST":
        form = DeliveryInfoForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    order = form.save(commit=False)
                    order.user = request.user
                    order.save()

                    borrowed_sets = []  # Store borrowed set names for email

                    # Create Borrowing records for each item
                    for item in cart_items:
                        borrowing = Borrowing.objects.create(
                            user=request.user,
                            lego_set=item.product,
                            is_returned=False,  # Marked as active borrowed set
                            subscription=request.user.userprofile.subscription
                        )

                        # Store borrowed LEGO set names for email
                        borrowed_sets.append(item.product.name)

                        # Decrease stock after borrowing
                        if item.product.stock > 0:
                            item.product.stock -= 1  # Reduce stock by 1
                            item.product.is_borrowed = True
                            item.product.save()

                        # **Create Notification for Borrowing**
                        Notification.objects.create(
                            user=request.user,
                            message=f"{request.user.username} borrowed {item.product.name}.",
                            category="borrowing"
                        )

                        # **Send Borrowing Confirmation Email**
                        subject = "LEGO Set Borrowing Confirmation"
                        context = {
                            'user': request.user,
                            'borrowed_sets': borrowed_sets,
                        }
                        email_html_message = render_to_string(
                            'allauth/account/borrow_confirmation.html', context
                        )
                        email_plain_message = strip_tags(email_html_message)

                        send_mail(
                            subject=subject,
                            message=email_plain_message,
                            from_email=settings.DEFAULT_FROM_EMAIL,
                            recipient_list=[request.user.email],
                            html_message=email_html_message,
                            fail_silently=False,
                        )

                    # Clear the cart after checkout
                    cart.items.all().delete()

                    messages.success(
                        request,
                        "Your LEGO set(s) have been successfully borrowed! "
                        "You can swap them anytime by returning sets."
                    )
                    return redirect("user_profile")  # Redirect to profile
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")
        else:
            messages.error(request, "Please correct the errors")

    else:
        form = DeliveryInfoForm()

    context = {
        "form": form,
        "cart_items": cart_items,
    }
    return render(request, "cart/checkout.html", context)
