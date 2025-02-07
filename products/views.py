from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from django.core.mail import send_mail
from django.contrib import messages
from django.utils.timezone import now
from .models import Product, Category, Review
from subscriptions.models import UserProfile, Subscription


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


@login_required
def add_review(request, product_id):
    """ Allow users to leave a review if they have a valid subscription """
    product = get_object_or_404(Product, id=product_id)

    # Check if user has an active subscription
    user_profile = UserProfile.objects.filter(user=request.user).first()
    has_subscription = user_profile and user_profile.subscription and user_profile.subscription.status
    if not has_subscription:
        messages.error(request, "You need an active subscription to leave a review.")
        return redirect('subscription_plans')

    # Check if user has already reviewed this LEGO set
    existing_review = Review.objects.filter(user=request.user, lego_set=product).exists()
    if existing_review:
        messages.warning(request, "You have already reviewed this LEGO set.")
        return redirect('product_detail', product_id=product.id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.lego_set = product
            review.save()

            # Notify admin of new review
            send_mail(
                subject="New Review Submitted",
                message=f"A new review was submitted by {request.user.username} for {product.name}.",
                from_email="sophiebmcgee@gmail.com",
                recipient_list=["sophiebmcgee@gmail.com"],
                fail_silently=True,
            )

            messages.success(request, "Your review has been posted successfully!")
            return redirect('product_detail', product_id=product.id)
        else:
            messages.error(request, "There was an error in your review submission. Please try again.")
    else:
        form = ReviewForm()

    return render(request, 'reviews/add_review.html', {'form': form, 'product': product})


@staff_member_required
def delete_review(request, review_id):
    """Allow only admin/superusers to delete reviews."""
    review = get_object_or_404(Review, id=review_id)
    product_id = review.product.id  # Ensure redirection after deletion
    review.delete()
    messages.success(request, "Review deleted successfully.")
    return redirect('product_detail', product_id=product_id)

