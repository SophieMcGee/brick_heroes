from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from orders.models import BorrowOrder, BorrowOrderItem
from .models import Cart, CartItem
from products.models import Product
from .forms import DeliveryInfoForm
from django.db import transaction
from django.utils.timezone import now


@login_required
def view_cart(request):
    """Display the borrowed LEGO sets."""
    cart, _ = Cart.objects.get_or_create(user=request.user)

    if not cart.items.exists():
        messages.info(request, "Your borrow cart is empty. Add LEGO sets to start borrowing.")

    context = {
        "cart": cart,
    }
    return render(request, "cart/shopping_cart.html", context)


@login_required
def add_to_cart(request, product_id):
    """Allow users to borrow LEGO sets based on their subscription plan."""
    cart, _ = Cart.objects.get_or_create(user=request.user)
    product = get_object_or_404(Product, id=product_id)

    # Ensure user has an active subscription
    if not request.user.userprofile.subscription or not request.user.userprofile.subscription.status:
        messages.error(request, "You need an active subscription to borrow LEGO sets.")
        return redirect("subscription_plans")

    # Get subscription limits
    subscription = request.user.userprofile.subscription
    active_borrows = CartItem.objects.filter(cart=cart).count()

    if active_borrows >= subscription.subscription_plan.max_active_borrows:
        messages.warning(
            request, 
            f"You have reached your borrowing limit of {subscription.subscription_plan.max_active_borrows} sets."
        )
        return redirect("shopping_cart")

    # Add LEGO set to cart
    CartItem.objects.get_or_create(cart=cart, product=product)
    messages.success(request, f"{product.name} has been added to your borrowed list!")
    return redirect("shopping_cart")


@login_required
def remove_from_cart(request, item_id):
    """Remove a borrowed LEGO set from the cart."""
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, id=item_id)

    messages.success(request, f"{cart_item.product.name} has been removed from your borrowed sets.")
    cart_item.delete()
    return redirect("shopping_cart")


@login_required
def checkout(request):
    """Handle the checkout process for borrowing LEGO sets."""
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = cart.items.all()

    if not cart_items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect("shopping_cart")

    if request.method == "POST":
        form = DeliveryInfoForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                # Create a new BorrowOrder
                order = form.save(commit=False)
                order.user = request.user
                order.save()

                # Create BorrowOrderItems for each item in the cart
                for item in cart_items:
                    BorrowOrderItem.objects.create(
                        order=order,
                        product=item.product,
                        quantity=1
                    )

                # Clear the cart after order is confirmed
                cart.items.all().delete()

                messages.success(request, "Your borrow order has been placed successfully! Your sets will be shipped soon.")
                return redirect("user_profile")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = DeliveryInfoForm()

    context = {
        "form": form,
        "cart_items": cart_items,
    }
    return render(request, "cart/checkout.html", context)

