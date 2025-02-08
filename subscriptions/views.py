import stripe
import json
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now, timedelta
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import SubscriptionPlan, Subscription, UserProfile, Borrowing
from django.contrib import messages
from notifications.models import Notification
from allauth.account.models import EmailAddress
from django.core.mail import send_mail
import logging

stripe.api_key = settings.STRIPE_SECRET_KEY


def subscription_plans(request):
    """A view to display all subscription plans."""
    plans = SubscriptionPlan.objects.all()
    return render(
        request,
        "subscriptions/subscription_plans.html",
        {
            "plans": plans,
            "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY,
        },
    )


@login_required
def subscription_confirmation(request, plan_id):
    """Displays the confirmation page before proceeding to Stripe checkout."""
    plan = get_object_or_404(SubscriptionPlan, pk=plan_id)

    return render(
        request,
        "subscriptions/subscription_confirmation.html",
        {"plan": plan},
    )


@login_required
def subscribe(request, plan_id):
    """Handles Stripe Checkout for subscription plans."""
    plan = get_object_or_404(SubscriptionPlan, pk=plan_id)

    # Ensure the plan has a Stripe Price ID
    if not plan.stripe_price_id:
        messages.error(request, "Subscription plan is missing a Stripe Price ID.")
        return redirect('subscription_plans')

    existing_subscription = Subscription.objects.filter(user=request.user, status=True).first()
    if existing_subscription:
        messages.warning(request, "You already have an active subscription.")
        return redirect('user_profile')

    try:
        # Fetch or Create Stripe Customer for the User
        if not request.user.userprofile.stripe_customer_id:
            customer = stripe.Customer.create(email=request.user.email)
            request.user.userprofile.stripe_customer_id = customer['id']
            request.user.userprofile.save()
        else:
            customer = stripe.Customer.retrieve(request.user.userprofile.stripe_customer_id)

        # Create Stripe Checkout Session using the existing Price ID
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            customer=customer.id,
            mode='subscription',
            line_items=[{
                'price': plan.stripe_price_id,  # Use existing Stripe Price ID
                'quantity': 1,
            }],
            success_url=request.build_absolute_uri(f"/subscriptions/success/"),
            cancel_url=request.build_absolute_uri('/subscriptions/cancel/'),
        )

        messages.success(request, f"Redirecting to Stripe for {plan.name} subscription...")

        subscription = Subscription.objects.create(
            user=request.user,
            subscription_plan=plan,
            stripe_subscription_id=session.id,
            start_date=now(),
            end_date=now() + timedelta(days=30),
            status=True,
        )

        user_profile = request.user.userprofile
        user_profile.subscription = subscription  # Link subscription to the UserProfile
        user_profile.save()
        
        return redirect(session.url)

    except stripe.error.StripeError as e:
        messages.error(request, f"Stripe error: {str(e)}")
        return redirect('subscription_plans')


@login_required
def cancel_subscription(request):
    """Cancels the user's Stripe subscription."""
    user_profile = get_object_or_404(UserProfile, user=request.user)

    if not user_profile.subscription:
        messages.error(request, "No active subscription to cancel.")
        return redirect('user_profile')

    # Cancel Stripe Subscription
    subscription = user_profile.subscription
    try:
        stripe.Subscription.modify(
            subscription.stripe_subscription_id,
            cancel_at_period_end=True  # Prevents auto-renewal
        )
        subscription.status = False
        subscription.save()
        messages.success(request, "Your subscription has been cancelled and will not renew.")
    except Exception as e:
        messages.error(request, f"Error cancelling subscription: {str(e)}")

    return redirect('user_profile')


@login_required
def renew_subscription(request):
    """Allows users to renew their subscription after expiry."""
    user_profile = get_object_or_404(UserProfile, user=request.user)

    if not user_profile.subscription or user_profile.subscription.status:
        messages.warning(request, "No expired subscription to renew.")
        return redirect('subscription_plans')

    # Extend the subscription by another month
    user_profile.subscription.start_date = now()
    user_profile.subscription.end_date = now() + timedelta(days=30)
    user_profile.subscription.status = True
    user_profile.subscription.save()

    messages.success(request, "Subscription renewed successfully!")
    return redirect('user_profile')


def check_and_update_subscriptions():
    """Function to auto-expire subscriptions and send reminders."""
    expired_subs = Subscription.objects.filter(status=True, end_date__lt=now())

    for sub in expired_subs:
        sub.status = False
        sub.save()
    
    # Send renewal reminder emails
    upcoming_renewals = Subscription.objects.filter(
        status=True,
        end_date__lte=now() + timedelta(days=7)
    )

    for sub in upcoming_renewals:
        send_mail(
            subject="Your Brick Heroes Subscription is Renewing Soon",
            message=f"Hello {sub.user.username},\n\nYour subscription will renew on {sub.end_date}. If you wish to cancel, please do so before the renewal date.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[sub.user.email],
        )

logger = logging.getLogger(__name__)

@csrf_exempt
def stripe_webhook(request):
    """Handles Stripe Webhook events."""
    payload = request.body
    sig_header = request.headers.get("Stripe-Signature", "")
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except (ValueError, stripe.error.SignatureVerificationError) as e:
        return JsonResponse({"error": str(e)}, status=400)

    logger.info(f"Stripe Webhook Event: {event['type']}")

    if event["type"] == "customer.subscription.created":
        subscription_data = event["data"]["object"]
        customer_id = subscription_data.get("customer")
        stripe_subscription_id = subscription_data.get("id")
        price_id = subscription_data["items"]["data"][0]["price"]["id"]

        # Debugging: Print Stripe IDs
        logger.info(f"Customer ID: {customer_id}")
        logger.info(f"Subscription ID: {stripe_subscription_id}")
        logger.info(f"Price ID: {price_id}")

        # Ensure we have a matching plan
        plan = SubscriptionPlan.objects.filter(stripe_price_id=price_id).first()
        if not plan:
            logger.warning(f"No matching SubscriptionPlan for Stripe Price ID: {price_id}")
            return JsonResponse({"error": "No matching plan"}, status=400)

        # Ensure we have a matching user
        user_profile = UserProfile.objects.filter(stripe_customer_id=customer_id).first()
        if not user_profile:
            logger.warning(f"No matching user for Stripe Customer ID: {customer_id}")
            return JsonResponse({"error": "No matching user"}, status=400)

        # Prevent creating duplicate subscriptions
        existing_subscription = Subscription.objects.filter(
            user=user_profile.user, status=True
        ).first()
        if existing_subscription:
            logger.info(f"Subscription already exists for {user_profile.user.username}. Skipping creation.")
            return JsonResponse({"message": "Subscription already exists"}, status=200)

        # Create the subscription
        subscription = Subscription.objects.create(
            user=user_profile.user,
            subscription_plan=plan,
            stripe_subscription_id=stripe_subscription_id,
            start_date=now(),
            end_date=now() + timedelta(days=30),
            status=True,
        )

        # Update user profile with subscription
        user_profile.subscription = subscription
        user_profile.save()

        logger.info(f"Subscription saved for {user_profile.user.username}")

        return JsonResponse({"message": "New subscription created"}, status=200)

    return JsonResponse({"message": "Unhandled event type"}, status=200)



def subscription_success(request):
    """Display subscription success message."""
    return render(request, "subscriptions/success.html")


def subscription_cancel(request):
    """Display subscription cancellation message."""
    return render(request, "subscriptions/cancel.html")


@login_required
def user_profile(request):
    """User profile page displaying subscriptions, emails, and borrowed sets."""
    user_profile = request.user.userprofile
    
    # Debugging line to check if UserProfile is linked correctly and subscription is available
    print(f"User Profile Subscription: {user_profile.subscription}")  # This should show the subscription object or None
    
    # Check if the user has an active subscription
    if user_profile.subscription and user_profile.subscription.status:
        subscription = user_profile.subscription
        subscription_plan_name = subscription.subscription_plan.name if subscription.subscription_plan else "No Plan"
    else:
        subscription = None
        subscription_plan_name = "No Active Subscription"

    # Debugging line to check subscription and subscription_plan_name values
    print(f"Subscription Status: {subscription_plan_name}")  # This should show the subscription name or "No Active Subscription"

    borrowed_sets = Borrowing.objects.filter(user=request.user, is_returned=False)
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')[:5]
    emailaddresses = EmailAddress.objects.filter(user=request.user)

    # Debugging line to check the borrowed sets and notifications
    print(f"Borrowed Sets Count: {borrowed_sets.count()}")  # Check how many sets are currently borrowed
    print(f"Notifications: {notifications}")  # Check the notifications
    
    messages.info(request, "Welcome back! Here is your subscription and borrowing summary.")

    return render(request, 'home/user_profile.html', {
        'user_profile': user_profile,
        'subscription': subscription,
        'subscription_plan_name': subscription_plan_name,
        'borrowed_sets': borrowed_sets,
        'notifications': notifications,
        'emailaddresses': emailaddresses,
    })
