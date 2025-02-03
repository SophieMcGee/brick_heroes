from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now, timedelta
from .models import SubscriptionPlan, Subscription, UserProfile
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from notifications.models import Notification

def subscription_plans(request):
    """A view to display all subscription plans."""
    plans = SubscriptionPlan.objects.all()
    return render(request, 'subscriptions/subscription_plans.html', {'plans': plans})

def subscribe(request, plan_id):
    """A view to handle user subscription."""
    plan = get_object_or_404(SubscriptionPlan, pk=plan_id)
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    # Check if the user already has an active subscription
    existing_subscription = Subscription.objects.filter(user=request.user, status=True).first()

    if existing_subscription:
        messages.warning(request, "You already have an active subscription.")
        return redirect('user_profile')

    # Set subscription start and end dates (e.g., 30 days duration)
    start_date = now()
    end_date = start_date + timedelta(days=30)

    # Create new subscription
    new_subscription = Subscription.objects.create(
        user=request.user,
        subscription_plan=plan,
        start_date=start_date,
        end_date=end_date,
        status=True
    )

    # Link the subscription to the user profile
    user_profile.subscription = new_subscription
    user_profile.save()

    Notification.objects.create(
        user=request.user,
        message=f"You've successfully subscribed to {plan.name}!"
    )

    return redirect('user_profile')


@login_required
def cancel_subscription(request):
    """View to cancel the user's current subscription."""
    user_profile = get_object_or_404(UserProfile, user=request.user)

    if not user_profile.subscription:
        messages.error(request, "You don't have an active subscription to cancel.")
        return redirect('user_profile')

    # Set subscription status to inactive
    user_profile.subscription.status = False
    user_profile.subscription.save()

    messages.success(request, "Your subscription has been cancelled.")
    return redirect('user_profile')

@login_required
def renew_subscription(request):
    """Allow users to renew their subscription after expiry."""
    user_profile = get_object_or_404(UserProfile, user=request.user)

    if not user_profile.subscription or user_profile.subscription.status:
        messages.warning(request, "You don't have an expired subscription to renew.")
        return redirect('subscription_plans')

    # Extend the subscription by another 30 days
    user_profile.subscription.start_date = now()
    user_profile.subscription.end_date = now() + timedelta(days=30)
    user_profile.subscription.status = True
    user_profile.subscription.save()

    messages.success(request, "Subscription renewed successfully!")
    return redirect('user_profile')

def check_and_update_subscriptions():
    """Function for homepage to auto-expire subscriptions."""
    check_expired_subscriptions()