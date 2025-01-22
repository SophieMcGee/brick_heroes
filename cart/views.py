from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem
from products.models import Product
from subscriptions.models import SubscriptionPlan

@login_required
def view_cart(request):
    """View the cart contents."""
    cart, _ = Cart.objects.get_or_create(user=request.user)
    return render(request, 'cart/cart.html', {'cart': cart})


@login_required
def add_to_cart(request, item_type, item_id):
    """Add a product or subscription to the cart."""
    cart, _ = Cart.objects.get_or_create(user=request.user)

    if item_type == "product":
        product = get_object_or_404(Product, id=item_id)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += 1
        cart_item.save()

    elif item_type == "subscription":
        subscription = get_object_or_404(SubscriptionPlan, id=item_id)
        # Remove any other subscription in the cart (if only one is allowed)
        CartItem.objects.filter(cart=cart, subscription__isnull=False).delete()
        CartItem.objects.get_or_create(cart=cart, subscription=subscription)

    return redirect('view_cart')


@login_required
def remove_from_cart(request, item_id):
    """Remove an item from the cart."""
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, id=item_id)
    cart_item.delete()
    return redirect('view_cart')


@login_required
def update_cart(request, item_id):
    """Update the quantity of a cart item."""
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, id=item_id)
    quantity = request.POST.get('quantity')
    if quantity:
        cart_item.quantity = int(quantity)
        cart_item.save()
    return redirect('view_cart')

def checkout(request):
    """Handle the checkout process."""
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = cart.items.all()

    # Separate subscription and product items
    subscription_item = None
    product_items = []

    for item in cart_items:
        if item.subscription:
            subscription_item = item
        elif item.product:
            product_items.append(item)

    # Redirect to subscription checkout if a subscription is in the cart
    if subscription_item:
        return redirect('subscription_checkout', subscription_id=subscription_item.subscription.id)

    # Proceed to normal checkout for products
    if product_items:
        return render(request, 'cart/product_checkout.html', {'cart': cart, 'product_items': product_items})

    # If the cart is empty, redirect back to the cart
    return redirect('view_cart')

def complete_product_checkout(request):
    """Complete product checkout."""
    cart = get_object_or_404(Cart, user=request.user)
    cart.items.filter(product__isnull=False).delete()
    return redirect('view_cart')
