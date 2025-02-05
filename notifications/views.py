from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Notification


@login_required
def user_notifications(request):
    """Displays all notifications for the logged-in user."""
    notifications = (
        Notification.objects.filter(user=request.user)
        .order_by('-created_at')
    )

    return render(
        request,
        'notifications/notifications.html',
        {'notifications': notifications},
    )


def admin_notifications(request):
    return render(request, "notifications/admin_notifications.html")