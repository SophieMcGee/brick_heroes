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

    return render(request, 'products/product_detail.html', {
        'product': product,
        'user_subscription': user_subscription,
        'subscription_valid': subscription_valid,
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
    """Handles rating submission via AJAX and updates average rating dynamically."""
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == "POST":
        rating_value = request.POST.get("rating")
        
        if not rating_value:
            return JsonResponse({"error": "No rating value provided"}, status=400)

        try:
            rating_value = int(rating_value)
            if rating_value < 1 or rating_value > 5:
                return JsonResponse({"error": "Invalid rating"}, status=400)
        except ValueError:
            return JsonResponse({"error": "Invalid rating input"}, status=400)

        # Save the new rating
        Rating.objects.create(product=product, rating=rating_value)

        # Update average rating
        avg_rating = product.get_average_rating()
        
        return JsonResponse({"message": "Rating submitted successfully", "new_avg_rating": avg_rating})

    return JsonResponse({"error": "Invalid request"}, status=400)

def submit_review(request, product_id):
    """Allows only subscribers to submit reviews for a product, pending admin approval."""
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        review_text = request.POST.get("review_text", "").strip()

        if not request.user.userprofile.subscription or not request.user.userprofile.subscription.status:
            messages.error(request, "You must be an active subscriber to leave a review.")
            return redirect("product_detail", product_id=product.id)

        Review.objects.create(
            user=request.user, product=product, content=review_text, is_approved=False
        )

        messages.success(request, "Your review has been submitted for approval.")
        return redirect("product_detail", product_id=product.id)

    return redirect("product_detail", product_id=product.id)