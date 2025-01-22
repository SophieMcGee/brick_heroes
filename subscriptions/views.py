from django.shortcuts import render, get_object_or_404, redirect
from .models import SubscriptionPlan, UserProfile
from django.contrib.auth.decorators import login_required

def subscription_plans(request):
    """A view to display all subscription plans."""
    plans = SubscriptionPlan.objects.all()
    return render(request, 'subscriptions/subscription_plans.html', {'plans': plans})

@login_required
def subscribe(request, plan_id):
    """A view to handle user subscription."""
    plan = get_object_or_404(SubscriptionPlan, pk=plan_id)
    user_profile = UserProfile.objects.get(user=request.user)
    user_profile.subscription = plan
    user_profile.save()
    return redirect('user_profile')

@login_required
def cancel_subscription(request):
    """View to cancel the user's current subscription"""
    user_profile = get_object_or_404(UserProfile, user=request.user)

    if not user_profile.subscription:
        messages.error(request, "You don't have an active subscription to cancel.")
        return redirect('user_profile')

    user_profile.subscription = None
    user_profile.save()

    messages.success(request, "Your subscription has been cancelled.")
    return redirect('user_profile')

def subscription_checkout(request, subscription_id):
    """Handle subscription checkout."""
    subscription = get_object_or_404(SubscriptionPlan, id=subscription_id)

    if request.method == "POST":
        user_profile = UserProfile.objects.get(user=request.user)
        user_profile.subscription = subscription
        user_profile.save()
        return redirect('user_profile')

    return render(request, 'subscriptions/subscription_checkout.html', {'subscription': subscription})