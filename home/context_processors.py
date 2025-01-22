from subscriptions.models import Borrowing
from cart.models import CartItem

def global_header_context(request):
    """Add global context variables for the header."""
    if request.user.is_authenticated:
        total_borrowed = Borrowing.objects.filter(user=request.user, is_returned=False).count()
        total_purchased = CartItem.objects.filter(cart__user=request.user, product__isnull=False).count()
    else:
        total_borrowed = 0
        total_purchased = 0

    return {
        'total_borrowed': total_borrowed,
        'total_purchased': total_purchased,
    }