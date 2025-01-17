from django.shortcuts import render
from .models import Product

def all_products(request):
    """ A view to show all products, with optional filters """

    # Get all products
    products = Product.objects.all()

    # Get filters from the query parameters
    difficulty = request.GET.get('difficulty')
    theme = request.GET.get('theme')

    # Filter by difficulty if provided
    if difficulty:
        products = products.filter(difficulty=difficulty)

    # Filter by theme if provided
    if theme:
        products = products.filter(category__friendly_name=theme)

    # Add filters to the context
    context = {
        'products': products,
        'current_difficulty': difficulty,
        'current_theme': theme,
    }

    return render(request, 'products/products.html', context)