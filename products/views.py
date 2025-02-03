from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Product, Category
from subscriptions.models import UserProfile


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

    # Check if user is subscribed & active
    user_subscription = None
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.filter(user=request.user).first()
        if user_profile and user_profile.subscription:
            if (
                user_profile.subscription.status and
                user_profile.subscription.end_date > now()
            ):
                user_subscription = user_profile.subscription
            else:
                messages.warning(
                    request,
                    "Your subscription has expired! Renew to borrow."
                )
                return redirect('renew_subscription')

    return render(request, 'products/product_detail.html', {
        'product': product,
        'user_subscription': user_subscription,
    })


def products_by_category(request, category_name):
    """Filter products by category."""
    products = Product.objects.filter(category__name=category_name)
    return render(
        request,
        'products/category_products.html',
        {
            'products': products,
            'category_name': category_name,
        },
    )
