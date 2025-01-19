from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Product, Category

def all_products(request):
    """ A view to show all products, with optional filters """

    # Get all products
    products = Product.objects.all()

    # Get filters from the query parameters
    query = request.GET.get('q')
    difficulty = request.GET.get('difficulty')
    theme = request.GET.get('theme')
    category = request.GET.get('category')

    # Define valid filters (optional)
    valid_difficulties = ['Beginner', 'Intermediate', 'Expert']
    valid_themes = Product.objects.values_list('category__friendly_name', flat=True).distinct()

    # Apply search filtering
    if query:
        # Filter products by name or description containing the query
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    # Filter by difficulty if provided and valid
    if difficulty in valid_difficulties:
        products = products.filter(difficulty__iexact=difficulty)

    # Filter by theme if provided and valid
    if theme in valid_themes:
        products = products.filter(category__friendly_name__iexact=theme)

    # Filter by category if provided
    if category:
        products = products.filter(category__name=category)

    # Convert category names to category objects for template use
    current_categories = Category.objects.filter(name__in=category.split(',')) if category else None

    # Add filters to the context
    context = {
        'products': products,
        'current_difficulty': difficulty if difficulty in valid_difficulties else None,
        'current_theme': theme if theme in valid_themes else None,
        'product_count': products.count(),
        'current_categories': current_categories,
        'search_term': query,
    }

    return render(request, 'products/products.html', context)

def product_detail(request, product_id):
    """ A view to show individual product details """
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'products/product_detail.html', {'product': product})