from subscriptions.models import Borrowing
from cart.models import CartItem
from notifications.models import Notification
from django.conf import settings

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

def admin_notification_count(request):
    """Adds the number of unread admin notifications to context for base.html."""
    if request.user.is_authenticated and request.user.is_superuser:
        return {
            'admin_notifications_count': Notification.objects.filter(is_read=False).count()
        }
    return {'admin_notifications_count': 0}

def media_url(request):
    """Make MEDIA_URL available globally in templates"""
    return {"MEDIA_URL": settings.MEDIA_URL}