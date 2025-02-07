import stripe
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
def subscribe(request, plan_id):
    """Handles Stripe Checkout for subscription plans."""
    plan = get_object_or_404(SubscriptionPlan, pk=plan_id)
    
    existing_subscription = Subscription.objects.filter(user=request.user, status=True).first()
    if existing_subscription:
        messages.warning(request, "You already have an active subscription.")
        return redirect('user_profile')

    try:
        # Create Stripe Checkout Session
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            customer_email=request.user.email,
            mode='subscription',
            line_items=[{
                'price_data': {
                    'currency': 'eur',
                    'product_data': {'name': plan.name},
                    'unit_amount': int(plan.price * 100),
                    'recurring': {'interval': 'month'},
                },
                'quantity': 1,
            }],
            customer_creation="if_required",  
            allow_promotion_codes=True, 
            automatic_tax={'enabled': False},
            success_url=request.build_absolute_uri(f"/subscriptions/success/?session_id={session.id}"),
            cancel_url=request.build_absolute_uri('/subscriptions/cancel/'),
        )

        messages.success(request, f"Redirecting to Stripe for {plan.name} subscription...")
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


@csrf_exempt
def stripe_webhook(request):
    """Handles Stripe Webhook events (e.g., subscription payments, cancellations)."""
    payload = request.body
    sig_header = request.headers.get("Stripe-Signature", "")
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)

        if event["type"] == "invoice.payment_succeeded":
            intent = event["data"]["object"]
            pid = intent["id"]

            # Get the latest charge object (UPDATED)
            latest_charge_id = intent.get("latest_charge")
            stripe_charge = stripe.Charge.retrieve(latest_charge_id) if latest_charge_id else None

            # Extract billing details (UPDATED)
            billing_details = stripe_charge["billing_details"] if stripe_charge else None
            shipping_details = intent.get("shipping", {})

            # Extract payment details (UPDATED)
            grand_total = round(stripe_charge["amount"] / 100, 2) if stripe_charge else 0

            customer_email = billing_details["email"] if billing_details else None
            if customer_email:
                user = get_object_or_404(UserProfile, user__email=customer_email)

                # Extend subscription
                user.subscription.end_date = now() + timedelta(days=30)
                user.subscription.status = True
                user.subscription.save()

                messages.success(request, "Your subscription payment was successful!")

        elif event["type"] == "customer.subscription.deleted":
            customer_email = event["data"]["object"].get("customer_email")
            if customer_email:
                user = get_object_or_404(UserProfile, user__email=customer_email)

                # Mark subscription as cancelled
                user.subscription.status = False
                user.subscription.save()
                messages.error(request, "Your subscription has been cancelled due to a failed payment.")

    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    return HttpResponse(status=200)


@login_required
def user_profile(request):
    """User profile page displaying subscriptions, emails, and borrowed sets."""
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    subscription = Subscription.objects.filter(user=request.user).first()
    borrowed_sets = Borrowing.objects.filter(user=request.user, is_returned=False)
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')[:5]
    emailaddresses = EmailAddress.objects.filter(user=request.user)

    messages.info(request, "Welcome back! Here is your subscription and borrowing summary.")

    return render(request, 'home/user_profile.html', {
        'user_profile': user_profile,
        'subscription': subscription,
        'borrowed_sets': borrowed_sets,
        'notifications': notifications,
        'emailaddresses': emailaddresses,
        'orders': orders,
    })
