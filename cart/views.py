from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cart, CartItem
from products.models import Product
from subscriptions.models import SubscriptionPlan


@login_required
def add_to_cart(request, item_type, item_id):
    """Add a subscription or Lego set to the cart based on the user's plan."""
    cart, _ = Cart.objects.get_or_create(user=request.user)

    # Check if user has a subscription
    user_subscription = CartItem.objects.filter(cart=cart, subscription__isnull=False).first()

    if item_type == "subscription":
        subscription = get_object_or_404(SubscriptionPlan, id=item_id)
        
        # Remove any previous subscription in the cart
        CartItem.objects.filter(cart=cart, subscription__isnull=False).delete()
        CartItem.objects.get_or_create(cart=cart, subscription=subscription)
        
        messages.success(request, f"You have selected the {subscription.name} plan!")
        return redirect('shopping_cart')

    elif item_type == "product":
        if not user_subscription:
            messages.error(request, "You need a subscription to borrow Lego sets.")
            return redirect('subscriptions')  # Redirect to subscription page

        product = get_object_or_404(Product, id=item_id)

        # Check borrowing limits
        borrowed_items = CartItem.objects.filter(cart=cart, product__isnull=False).count()
        max_borrow = user_subscription.subscription.max_active_borrows  # Get limit from subscription

        if borrowed_items >= max_borrow:
            messages.error(request, f"You've reached your borrowing limit of {max_borrow} sets.")
            return redirect('shopping_cart')

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += 1  # Increment if already in cart
        cart_item.save()

        messages.success(request, f"{product.name} has been added to your cart!")
        return redirect('shopping_cart')

    messages.error(request, "Invalid request method.")
    return redirect('shopping_cart')

@login_required
def view_cart(request):
    """Display the user's shopping cart."""
    cart, _ = Cart.objects.get_or_create(user=request.user)
    context = {
        'cart': cart,
    }
    return render(request, 'cart/shopping_cart.html', context)

@login_required
def remove_from_cart(request, item_id):
    """Remove an item from the cart (either subscription or borrowed sets)."""
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, id=item_id)

    if cart_item.subscription:
        # If removing a subscription, also remove all borrowed sets
        CartItem.objects.filter(cart=cart, product__isnull=False).delete()
        messages.success(request, f"Subscription {cart_item.subscription.name} and all borrowed sets have been removed.")
    elif cart_item.product:
        messages.success(request, f"{cart_item.product.name} removed from your cart.")

    cart_item.delete()
    return redirect('shopping_cart')

@login_required
def checkout(request):
    """Handle checkout for subscriptions and borrowed Lego sets."""
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = cart.items.all()

    # Get user's subscription
    subscription_item = cart_items.filter(subscription__isnull=False).first()
    borrowed_items = cart_items.filter(product__isnull=False)

    if not subscription_item:
        messages.error(request, "You must select a subscription before checking out.")
        return redirect('subscriptions')

    # Ensure user is within borrowing limits
    max_borrow = subscription_item.subscription.max_active_borrows
    if borrowed_items.count() > max_borrow:
        messages.error(request, f"You're exceeding your limit of {max_borrow} borrowed sets.")
        return redirect('shopping_cart')

    if request.method == "POST":
        # Assign subscription to user profile
        user_profile = request.user.userprofile
        user_profile.subscription = subscription_item.subscription
        user_profile.save()

        # Mark Lego sets as borrowed
        borrowed_items.delete()  # Clear the cart after checkout

        messages.success(request, "Your subscription is active! Your Lego sets will be delivered soon.")
        return redirect('dashboard')

    context = {
        'subscription': subscription_item.subscription,
        'borrowed_items': borrowed_items
    }
    return render(request, 'cart/subscription_checkout.html', context)

@login_required
def subscription_checkout(request, subscription_id):
    """Checkout view for a subscription and confirm borrowed sets."""
    subscription = get_object_or_404(SubscriptionPlan, id=subscription_id)
    cart = get_object_or_404(Cart, user=request.user)

    if request.method == "POST":
        # Assign the subscription to the user
        user_profile = request.user.userprofile
        user_profile.subscription = subscription
        user_profile.save()

        # Clear the cart after checkout
        CartItem.objects.filter(cart=cart).delete()
        
        messages.success(request, f"You have successfully subscribed to {subscription.name} and confirmed your borrowed sets!")
        return redirect('dashboard')

    context = {'subscription': subscription}
    return render(request, 'cart/subscription_checkout.html', context)