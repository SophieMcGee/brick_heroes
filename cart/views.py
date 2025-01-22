from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cart, CartItem
from products.models import Product
from subscriptions.models import SubscriptionPlan

@login_required
def shopping_cart(request):
    """View the shopping cart contents."""
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()

    # Calculate total
    cart_total = sum(
        item.product.price * item.quantity if item.product else item.subscription.price
        for item in cart_items
    )

    context = {
        'cart': cart,
        'cart_total': cart_total,
    }
    return render(request, 'cart/shopping_cart.html', context)


@login_required
def add_to_cart(request, item_type, item_id):
    """Add a product or subscription to the cart."""
    if request.method == "POST":
        cart, _ = Cart.objects.get_or_create(user=request.user)

        if item_type == "product":
            product = get_object_or_404(Product, id=item_id)
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            if not created:
                cart_item.quantity += 1
            cart_item.save()
            messages.success(request, f"{product.name} has been added to your cart!")

        elif item_type == "subscription":
            subscription = get_object_or_404(SubscriptionPlan, id=item_id)
            # Remove any other subscription in the cart
            CartItem.objects.filter(cart=cart, subscription__isnull=False).delete()
            CartItem.objects.get_or_create(cart=cart, subscription=subscription)
            messages.success(request, f"Subscription {subscription.name} added to your cart!")

        return redirect('shopping_cart')

    messages.error(request, "Invalid request method.")
    return redirect('shopping_cart')


@login_required
def remove_from_cart(request, item_id):
    """Remove an item from the cart."""
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, id=item_id)
    if cart_item.product:
        messages.success(request, f"{cart_item.product.name} removed from your cart.")
    elif cart_item.subscription:
        messages.success(request, f"Subscription {cart_item.subscription.name} removed from your cart.")
    cart_item.delete()
    return redirect('shopping_cart')


@login_required
def update_cart(request, item_id):
    """Update the quantity of a cart item."""
    if request.method == "POST":
        cart = get_object_or_404(Cart, user=request.user)
        cart_item = get_object_or_404(CartItem, cart=cart, id=item_id)
        quantity = request.POST.get('quantity')
        if quantity and int(quantity) > 0:
            cart_item.quantity = int(quantity)
            cart_item.save()
            messages.success(request, f"Updated quantity of {cart_item.product.name if cart_item.product else 'Subscription'} to {quantity}.")
        else:
            messages.error(request, "Invalid quantity.")
    return redirect('shopping_cart')


@login_required
def checkout(request):
    """Handle the checkout process."""
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = cart.items.all()

    # Separate subscription and product items
    subscription_item = cart_items.filter(subscription__isnull=False).first()
    product_items = cart_items.filter(product__isnull=False)

    if subscription_item:
        return redirect('subscription_checkout', subscription_id=subscription_item.subscription.id)

    if product_items.exists():
        return redirect('product_checkout')

    messages.error(request, "Your cart is empty.")
    return redirect('shopping_cart')


@login_required
def product_checkout(request):
    """Checkout view for products."""
    cart = get_object_or_404(Cart, user=request.user)
    product_items = cart.items.filter(product__isnull=False)

    if request.method == "POST":
        # Process checkout logic for products
        product_items.delete()
        messages.success(request, "Your product purchase was successful!")
        return redirect('shopping_cart')

    context = {'product_items': product_items}
    return render(request, 'cart/product_checkout.html', context)


@login_required
def subscription_checkout(request, subscription_id):
    """Checkout view for a subscription."""
    subscription = get_object_or_404(SubscriptionPlan, id=subscription_id)

    if request.method == "POST":
        # Assign the subscription to the user
        user_profile = request.user.userprofile
        user_profile.subscription = subscription
        user_profile.save()
        CartItem.objects.filter(cart__user=request.user, subscription=subscription).delete()
        messages.success(request, f"You have successfully subscribed to {subscription.name}!")
        return redirect('shopping_cart')

    context = {'subscription': subscription}
    return render(request, 'cart/subscription_checkout.html', context)