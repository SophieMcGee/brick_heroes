from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .models import Notification
from products.models import Review  # Import reviews from products

@staff_member_required
def admin_notifications(request):
    """Displays pending reviews, subscriptions, and borrowing notifications."""

    print("DEBUG: Fetching admin notifications...")

    # Fetch pending reviews (not yet approved)
    pending_reviews = Review.objects.filter(is_approved=False)

    # Fetch subscription notifications
    subscription_notifications = Notification.objects.filter(
        category="subscription"
    ).order_by('-created_at')

    # Fix: Ensure borrowing/return notifications are included
    borrowing_notifications = Notification.objects.filter(
        category="borrowing"
    ).order_by('-created_at')

    review_notifications = Notification.objects.filter(
        category="review"
    ).order_by('-created_at')

    print(f"DEBUG: Pending Reviews Count: {pending_reviews.count()}")
    print(f"DEBUG: Borrowing Notifications Count: {borrowing_notifications.count()}")

    return render(
        request,
        "notifications/admin_notifications.html",
        {
            "pending_reviews": pending_reviews,
            "subscription_notifications": subscription_notifications,
            "borrowing_notifications": borrowing_notifications,
            "review_notifications": review_notifications,
        },
    )


@staff_member_required
def approve_review(request, review_id):
    """Admin action to approve a pending review."""
    review = get_object_or_404(Review, id=review_id)
    review.is_approved = True
    review.save()
    messages.success(request, "Review approved successfully.")
    return redirect("admin_notifications")


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

@staff_member_required
def delete_notification(request, notification_id):
    """Allows admins to delete notifications."""
    notification = get_object_or_404(Notification, id=notification_id)
    notification.delete()
    messages.success(request, "Notification deleted successfully.")
    return redirect("admin_notifications")
