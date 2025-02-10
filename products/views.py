from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from django.core.mail import send_mail
from django.contrib import messages
from django.utils.timezone import now
from .models import Product, Rating, Review
from subscriptions.models import UserProfile, Subscription
from notifications.models import Notification
from .forms import ReviewForm


def all_products(request, category_name=None):
    """ A view to show all products, with optional filters """
    # Get all products
    products = Product.objects.all()

    # Apply category filter if category_name is provided
    if category_name:
        products = products.filter(category__name=category_name)

    # Get search query
    query = request.GET.get('q')
    if query:
        # Filter products by name or description containing the query
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
        # Add a success message to display the search term
        messages.success(request, f"Search results for: {query}")

    # Get filters from the query parameters
    difficulty = request.GET.get('difficulty')
    theme = request.GET.get('theme')
    sort_by = request.GET.get('sort_by')

    # Filter by difficulty
    if difficulty:
        products = products.filter(difficulty__iexact=difficulty)

    # Filter by theme
    if theme:
        products = products.filter(category__friendly_name__iexact=theme)

    # Sorting logic
    if sort_by == "name_asc":
        products = products.order_by('name')
    elif sort_by == "name_desc":
        products = products.order_by('-name')
    elif sort_by == "rating":
        products = products.order_by('-rating')

    if not products.exists():
        messages.warning(request, "No LEGO sets found matching your criteria.")

    context = {
        'products': products,
        'current_difficulty': difficulty,
        'current_theme': theme,
        'valid_themes': (
            Product.objects
            .values_list('category__friendly_name', flat=True)
            .distinct()
        ),
        'difficulties': (
            Product.objects
            .values_list('difficulty', flat=True)
            .distinct()
        ),
        'category_name': category_name,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """A view to show individual product details"""
    product = get_object_or_404(Product, id=product_id)

    # Default: No active subscription
    user_subscription = None
    subscription_valid = False

    if request.user.is_authenticated:
        user_profile = UserProfile.objects.filter(user=request.user).first()
        
        if user_profile:
            user_subscription = Subscription.objects.filter(user=request.user, status=True).first()
            if user_subscription and user_subscription.end_date and user_subscription.end_date > now():
                subscription_valid = True

    approved_reviews = product.reviews.filter(is_approved=True)

    return render(request, 'products/product_detail.html', {
        'product': product,
        'user_subscription': user_subscription,
        'subscription_valid': subscription_valid,
        'approved_reviews': approved_reviews,
    })


def products_by_category(request, category_name):
    """Filter products by category."""
    products = Product.objects.filter(category__name=category_name)

    if not products.exists():
        messages.info(request, f"No LEGO sets found in {category_name} category.")

    return render(
        request,
        'products/category_products.html',
        {
            'products': products,
            'category_name': category_name,
        },
    )


def submit_rating(request, product_id):
    """Handles rating submission and updates average rating dynamically."""
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        rating_value = request.POST.get("rating")

        if not rating_value:
            messages.warning(request, "⚠ Please select a rating before submitting.")
            print("DEBUG: Rating not provided")
            return redirect("product_detail", product_id=product.id)

        try:
            rating_value = int(rating_value)
            if rating_value < 1 or rating_value > 5:
                messages.warning(request, "⚠ Invalid rating value.")
                print("DEBUG: Invalid rating value")
                return redirect("product_detail", product_id=product.id)
        except ValueError:
            messages.warning(request, "⚠ Invalid rating input.")
            print("DEBUG: ValueError in rating")
            return redirect("product_detail", product_id=product.id)

        # Save the new rating
        Rating.objects.create(product=product, rating=rating_value)

        #  Update product rating immediately
        product.update_rating()

        messages.success(request, "⭐ Rating submitted successfully!")
        print("DEBUG: Success message set")

        return redirect("product_detail", product_id=product.id)


def submit_review(request, product_id):
    """Allows only subscribers to submit reviews for a product, pending admin approval."""
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        review_text = request.POST.get("review_text", "").strip()

        if not request.user.userprofile.subscription or not request.user.userprofile.subscription.status:
            messages.error(request, "You must be an active subscriber to leave a review.")
            return redirect("product_detail", product_id=product.id)

        # Check if a pending review exists to avoid duplication
        existing_review = Review.objects.filter(
            user=request.user, product=product, is_approved=False
        ).first()

        if existing_review:
            messages.warning(request, "You already have a pending review for this product.")
            return redirect("product_detail", product_id=product.id)

        # Create the review if no pending review exists
        Review.objects.create(
            user=request.user, product=product, content=review_text, is_approved=False
        )

        # Avoid duplicate notifications by checking existing ones
        if not Notification.objects.filter(user=request.user, content__icontains="review submitted").exists():
            Notification.objects.create(
                user=request.user,
                content=f"Your review for {product.name} has been submitted for approval.",
                link=f"/products/{product.id}/"
            )

        messages.success(request, "Your review has been submitted for approval.")
        return redirect("product_detail", product_id=product.id)

    return redirect("product_detail", product_id=product.id)


@login_required
def edit_review(request, product_id, review_id):
    """Allows users to edit their own approved reviews."""
    review = get_object_or_404(Review, id=review_id, product_id=product_id, user=request.user)

    if request.method == "POST":
        review_text = request.POST.get("review_text", "").strip()
        
        if review_text:
            review.content = review_text  # Update review text
            review.save()
            messages.success(request, "Your review has been updated successfully!")
        else:
            messages.error(request, "Review content cannot be empty.")

        return redirect("product_detail", product_id=product_id)

    return redirect("product_detail", product_id=product_id)

@login_required
def delete_review(request, review_id):
    """Allows users to delete their own reviews."""
    review = get_object_or_404(Review, id=review_id)

    # Ensure only the review's owner can delete it
    if review.user != request.user:
        messages.error(request, "You are not authorized to delete this review.")
        return redirect("product_detail", product_id=review.product.id)

    if request.method == "POST":  # Only allow DELETE via POST
        product_id = review.product.id  # Save product_id before deletion
        review.delete()
        messages.success(request, "Your review has been deleted successfully.")
        return redirect("product_detail", product_id=product_id)

    messages.error(request, "Invalid request.")
    return redirect("product_detail", product_id=review.product.id)



@staff_member_required
def approve_review(request, review_id):
    """Admin action to approve a pending review."""
    review = get_object_or_404(Review, id=review_id)
    review.is_approved = True
    review.save()

    # Ensure the product rating updates when a review is approved
    product = review.product
    product.update_rating()

    messages.success(request, "Review approved successfully.")
    return redirect("admin_notifications")