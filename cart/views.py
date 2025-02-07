from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
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
        messages.error(request, f"You have reached your borrowing limit of {subscription.subscription_plan.max_active_borrows} sets.")
        return redirect("shopping_cart")

    # Add LEGO set to cart
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if created:
        messages.success(request, f"{product.name} has been added to your borrow cart!")
    else:
        messages.info(request, f"{product.name} is already in your borrow cart.")

    return redirect("shopping_cart")


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

    if request.method == "POST":
        form = DeliveryInfoForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    order = form.save(commit=False)
                    order.user = request.user
                    order.save()

                    for item in cart_items:
                        Borrowing.objects.create(
                            user=request.user,
                            lego_set=item.product,
                            is_returned=False
                        )
                    cart.items.all().delete()
                    messages.success(request, "Your borrow order has been placed successfully!")
                    return redirect("user_profile")
            except Exception as e:
                messages.error(request, f"An error occurred while processing your order: {str(e)}")
        else:
            messages.error(request, "Please correct the errors in your delivery details.")

    else:
        form = DeliveryInfoForm()

    context = {
        "form": form,
        "cart_items": cart_items,
    }
    return render(request, "cart/checkout.html", context)

@login_required
def request_mystery_set(request):
    """Allow users with Mystery Subscription to request a set."""
    user_profile = request.user.userprofile
    subscription = user_profile.subscription

    print(user_profile.has_requested_mystery_set())

    # Ensure the user has the Mystery Subscription
    if not subscription or subscription.subscription_plan.name != "Mystery Subscription":
        messages.error(request, "You must have a Mystery Subscription to request a set.")
        return redirect('user_profile')

    # Check if the user has already requested a set this month
    if CartItem.objects.filter(cart__user=request.user, product__category__name='Mystery').filter(added_on__month=now().month).exists():
        messages.warning(request, "You have already requested a mystery set for this month.")
        return redirect('user_profile')

    # Assign a random mystery set from the available sets
    mystery_set = Product.objects.filter(category__name='Mystery', is_borrowed=False).first()
    if mystery_set:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=mystery_set)

        if created:
            messages.success(request, f"{mystery_set.name} has been added to your borrow cart!")

        # Mark the set as borrowed and save the cart item
        mystery_set.is_borrowed = True
        mystery_set.save()

        # Redirect user to the delivery details page
        return redirect('checkout')

    messages.error(request, "No mystery sets available at the moment.")
    return redirect('user_profile')

