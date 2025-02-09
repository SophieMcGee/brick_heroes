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
    """Allow users to borrow LEGO sets based on their subscription plan."""
    product = get_object_or_404(Product, id=product_id)

    # 1 Ensure user has an active subscription
    subscription = request.user.userprofile.subscription
    if not subscription or not subscription.status:
        messages.error(request, "You need an active subscription to borrow LEGO sets.")
        return redirect("subscription_plans")

    #  Get subscription limits
    max_active_borrows = subscription.subscription_plan.max_active_borrows

    # Check how many sets are currently borrowed (not returned)
    active_borrows = Borrowing.objects.filter(user=request.user, is_returned=False).count()

    # Restrict borrowing if limit reached
    if active_borrows >= max_active_borrows:
        messages.error(
            request,
            f"You have reached your borrowing limit of {max_active_borrows} sets. "
            f"Return a set to borrow a new one."
        )
        return redirect("shopping_cart")

    # **Create a Borrowing record** (instead of just adding to cart)
    borrowing = Borrowing.objects.create(
        user=request.user,
        lego_set=product,
        is_returned=False,
        subscription=subscription  # Ensure subscription is set
    )

    # Reduce stock for the borrowed set
    if product.stock > 0:
        product.stock -= 1
        product.is_borrowed = True  # Mark it as borrowed
        product.save()

    # **Create a notification for borrowing**
    Notification.objects.create(
        user=request.user,
        message=f"{request.user.username} borrowed {product.name}.",
        category="borrowing"
    )

    # Show success message & redirect
    messages.success(request, f"{product.name} has been added to your borrowed sets!")
    return redirect("user_profile")  # Redirect to the profile where borrowed sets are shown



@login_required
def remove_from_cart(request, item_id):
    """Remove a borrowed LEGO set from the cart."""
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, id=item_id)

    try:
        cart_item.delete()
        messages.success(request, f"{cart_item.product.name} has been removed from your borrow cart.")
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

    # Get borrowing limit from subscription
    max_active_borrows = subscription.subscription_plan.max_active_borrows if subscription else 0

    # Count active borrowed sets
    active_borrows = Borrowing.objects.filter(user=request.user, is_returned=False).count()

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

                    # Create Borrowing records for each item
                    for item in cart_items:
                        borrowing = Borrowing.objects.create(
                            user=request.user,
                            lego_set=item.product,
                            is_returned=False,  # Marked as active borrowed set
                            subscription=request.user.userprofile.subscription
                        )

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
                        print(f"DEBUG: Notification created for borrowing {item.product.name}")

                    # Clear the cart after checkout
                    cart.items.all().delete()

                    messages.success(
                        request, 
                        "Your LEGO set(s) have been successfully borrowed! "
                        "You can swap them anytime by returning sets."
                    )
                    return redirect("user_profile")  # Redirect to profile after success
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")
        else:
            messages.error(request, "Please correct the errors in your delivery details.")

    else:
        form = DeliveryInfoForm()

    context = {
        "form": form,
        "cart_items": cart_items,
    }
    return render(request, "cart/checkout.html", context)
