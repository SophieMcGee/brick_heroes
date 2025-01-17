from django.shortcuts import render
from django.db.models import Q
from .models import Product

def all_products(request):
    """ A view to show all products, with optional filters """

    # Get all products
    products = Product.objects.all()

    # Get filters from the query parameters
    difficulty = request.GET.get('difficulty')
    theme = request.GET.get('theme')

    # Define valid filters (optional)
    valid_difficulties = ['Beginner', 'Intermediate', 'Expert']
    valid_themes = Product.objects.values_list('category__friendly_name', flat=True).distinct()

    # Filter by difficulty if provided and valid
    if difficulty in valid_difficulties:
        products = products.filter(difficulty__iexact=difficulty)

    # Filter by theme if provided and valid
    if theme in valid_themes:
        products = products.filter(category__friendly_name__iexact=theme)

    # Add filters to the context
    context = {
        'products': products,
        'current_difficulty': difficulty if difficulty in valid_difficulties else None,
        'current_theme': theme if theme in valid_themes else None,
        'product_count': products.count(),
    }

    return render(request, 'products/products.html', context)
