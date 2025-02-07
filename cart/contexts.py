from .models import Cart

def cart_contents(request):
    """Make cart item count available in templates (only borrowed LEGO sets)"""
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        total_items = cart.items.filter(product__isnull=False).count()
    else:
        total_items = 0
    return {
        'cart_item_count': total_items,
    }
