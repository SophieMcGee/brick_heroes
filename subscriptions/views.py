import stripe
import json
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now, timedelta
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import SubscriptionPlan, Subscription, UserProfile, Borrowing
from cart.models import BorrowOrder
from django.contrib import messages
from notifications.models import Notification
from allauth.account.models import EmailAddress
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
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

    # Retrieve Stripe Checkout URL
    stripe_checkout_url = request.session.get('stripe_checkout_url')

    if not stripe_checkout_url:
        messages.error(
            request, "Error: Stripe checkout URL not found. Please try again."
        )
        return redirect('subscription_plans')

    return render(
        request,
        "subscriptions/subscription_confirmation.html",
        {"plan": plan, "stripe_checkout_url": stripe_checkout_url},
    )


@login_required
def subscribe(request, plan_id):
    """Handles Stripe Checkout for subscription plans with a confirmation."""
    plan = get_object_or_404(SubscriptionPlan, pk=plan_id)

    # Ensure the plan has a Stripe Price ID
    if not plan.stripe_price_id:
        messages.error(request, "Sub plan is missing a Stripe Price ID.")
        return redirect('subscription_plans')

    existing_subscription = Subscription.objects.filter(
        user=request.user, status=True
    ).first()

    if existing_subscription:
        messages.warning(request, "You already have an active subscription.")
        return redirect('user_profile')

    try:
        # Fetch or Create Stripe Customer for the User
        user_profile = request.user.userprofile

        if not user_profile.stripe_customer_id:
            # Always create a new Stripe customer if the old one was deleted
            customer = stripe.Customer.create(email=request.user.email)
            user_profile.stripe_customer_id = customer['id']
            user_profile.save()
        else:
            try:
                customer = stripe.Customer.retrieve(
                    user_profile.stripe_customer_id
                )
                # If customer was deleted, create a new one
                if customer.get("deleted", False):
                    customer = stripe.Customer.create(email=request.user.email)
                    user_profile.stripe_customer_id = customer['id']
                    user_profile.save()

            except stripe.error.InvalidRequestError:
                # If Stripe says the customer doesn't exist, create a new one
                customer = stripe.Customer.create(email=request.user.email)
                user_profile.stripe_customer_id = customer['id']
                user_profile.save()

        # Create Stripe Checkout Session using the existing Price ID
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            customer=customer.id,
            mode='subscription',
            line_items=[{
                'price': plan.stripe_price_id,
                'quantity': 1,
            }],
            success_url=request.build_absolute_uri(f"/subscriptions/success/"),
            cancel_url=request.build_absolute_uri('/subscriptions/cancel/'),
            metadata={"plan_id": str(plan.id)}
        )

        # Store session URL in session storage
        request.session['stripe_checkout_url'] = session.url
        request.session['stripe_checkout_session_id'] = session.id
        request.session['selected_plan_id'] = plan_id  # Save selected plan
        request.session.modified = True  # Ensure the session is saved

        # Create a Subscription Notification for Admin**
        Notification.objects.create(
            user=request.user,
            message=f"{request.user.username} has subscribed to {plan.name}.",
            category="subscription"
        )

        # Subscription Confirmation Email
        subject = "Subscription Confirmation - Brick Heroes"
        context = {'user': request.user, 'plan': plan}
        email_html_message = render_to_string('allauth/account/subscription_confirmation.html', context)
        email_plain_message = strip_tags(email_html_message)

        send_mail(
            subject=subject,
            message=email_plain_message,  # Plain text fallback
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[request.user.email],
            html_message=email_html_message,  # HTML email version
            fail_silently=False,
        )
        # Redirect user to the confirmation page
        return redirect('subscription_confirmation', plan_id=plan.id)

    except stripe.error.StripeError as e:
        print(f"Stripe Error: {e}")
        messages.error(request, f"Stripe error: {str(e)}")
        return redirect('subscription_plans')


@login_required
def cancel_subscription(request):
    """Cancels the Stripe subscription but keeps it active until expiry."""
    user_profile = get_object_or_404(UserProfile, user=request.user)

    if not user_profile.subscription:
        messages.error(request, "No active subscription to cancel.")
        return redirect('user_profile')

    subscription = user_profile.subscription

    if not subscription.stripe_subscription_id:
        messages.error(request, "Error: No valid Stripe subscription ID found")
        return redirect('user_profile')

    try:
        # Retrieve subscription from Stripe
        stripe_sub = stripe.Subscription.retrieve(
            subscription.stripe_subscription_id
        )

        if stripe_sub.status != "canceled":
            stripe.Subscription.modify(
                subscription.stripe_subscription_id,
                cancel_at_period_end=True  # Prevents auto-renewal
            )
            subscription.status = True  # Keep marked as active
            subscription.save()

            messages.success(
                request, "Your will remain active until the cancellation date."
            )

            # Send Cancellation Confirmation Email
            subject = "Subscription Cancellation Confirmation - Brick Heroes"
            context = {
                'user': request.user,
                'subscription': subscription,
            }
            email_html_message = render_to_string(
                'allauth/account/subscription_cancellation_email.html', context
            )
            email_plain_message = strip_tags(email_html_message)

            send_mail(
                subject=subject,
                message=email_plain_message,  # Plain text fallback
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[request.user.email],
                html_message=email_html_message,  # HTML email version
                fail_silently=False,
            )

        else:
            messages.info(request, "This subscription was already canceled.")

    except stripe.error.InvalidRequestError as e:
        print(f"Stripe API Error: {str(e)}")
        if "No such subscription" in str(e):
            subscription.status = False
            subscription.save()
            user_profile.subscription = None  # Unlink from profile
            user_profile.save()
            messages.error(
                request, "Your subscription was already canceled or removed."
            )

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
    """Auto-expire subscriptions and update accordingly."""
    expired_subs = Subscription.objects.filter(status=True, end_date__lt=now())

    for sub in expired_subs:
        if sub.stripe_subscription_id:
            try:
                stripe_sub = stripe.Subscription.retrieve(
                    sub.stripe_subscription_id
                )
                if stripe_sub.status == "canceled":
                    sub.status = False  # Mark as expired
                    sub.save()
                    logger.info(
                        f" Subscription expired: {sub.user.email} (ID: {sub.id})"
                    )

            except stripe.error.StripeError as e:
                logger.error(
                    f"Error checking Stripe subscription {sub.stripe_subscription_id}: "
                    f"{str(e)}"
                )

    # Send renewal reminder emails
    upcoming_renewals = Subscription.objects.filter(
        status=True,
        end_date__lte=now() + timedelta(days=7)
    )

    for sub in upcoming_renewals:
        send_mail(
            subject="Your Brick Heroes Subscription is Renewing Soon",
            message=(
                f"Hello {sub.user.username},\n\nYour subscription renews on "
                f"{sub.end_date}. If you wish to cancel, please do so before "
                f"renewal date."
            ),
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
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except (ValueError, stripe.error.SignatureVerificationError) as e:
        return JsonResponse({"error": str(e)}, status=400)

    logger.info(f"Stripe Webhook Event: {event['type']}")

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        customer_id = session.get("customer")
        stripe_subscription_id = session.get("subscription")

        user_profile = UserProfile.objects.filter(stripe_customer_id=customer_id).first()
        if not user_profile:
            logger.error("No matching user found for this checkout session.")
            return JsonResponse({"error": "No matching user"}, status=400)

        if not stripe_subscription_id:
            logger.error("No subscription ID found in checkout session.")
            return JsonResponse({"error": "No subscription found"}, status=400)

        plan_id = session.get("metadata", {}).get("plan_id")
        plan = SubscriptionPlan.objects.filter(id=plan_id).first()
        if not plan:
            logger.error("No matching subscription plan found.")
            return JsonResponse({"error": "No matching plan"}, status=400)

        # Check if the user already has a subscription
        existing_subscription = Subscription.objects.filter(user=user_profile.user).order_by('-end_date').first()

        if existing_subscription:
            # Only update if it's expired
            if existing_subscription.status is False:
                existing_subscription.subscription_plan = plan
                existing_subscription.stripe_subscription_id = stripe_subscription_id  # Save correct ID!
                existing_subscription.start_date = now()
                existing_subscription.end_date = now() + timedelta(days=30)
                existing_subscription.status = True
                existing_subscription.save()
                user_profile.subscription = existing_subscription
                user_profile.save()
                logger.info(
                    f" Subscription reactivated for {user_profile.user.email} (ID: {existing_subscription.id})"
                )
            else:
                logger.info(f" Subscription already exists for {user_profile.user.email} (ID: {existing_subscription.id})")
        else:
            # Create a new subscription if none exists
            subscription = Subscription.objects.create(
                user=user_profile.user,
                subscription_plan=plan,
                stripe_subscription_id=stripe_subscription_id,
                start_date=now(),
                end_date=now() + timedelta(days=30),
                status=True,
            )
            user_profile.subscription = subscription
            user_profile.save()
            logger.info(
                f"New subscription created for {user_profile.user.email}")

        return JsonResponse({"message": "Subscription processed successfully"}, status=200)

    elif event["type"] == "customer.subscription.deleted":
        stripe_subscription_id = event["data"]["object"]["id"]
        subscription = Subscription.objects.filter(stripe_subscription_id=stripe_subscription_id).first()

        if subscription:
            subscription.status = False
            subscription.save()
            logger.info(
                f" Subscription {stripe_subscription_id} marked as expired."
            )

    return JsonResponse({"message": "Webhook received"}, status=200)


@login_required
def subscription_success(request):
    """Creates a subscription in the database only after successful payment."""
    plan_id = request.session.get("selected_plan_id")
    if not plan_id:
        messages.error(request, "No subscription plan found. Please try again.")
        return redirect("user_profile")

    plan = get_object_or_404(SubscriptionPlan, pk=plan_id)

    # Check if the user already has a subscription (double-check)
    existing_subscription = Subscription.objects.filter(user=request.user, status=True).first()
    if existing_subscription:
        messages.warning(request, "You already have an active subscription.")
        return redirect("user_profile")

    # Create the subscription **after** payment success
    subscription = Subscription.objects.create(
        user=request.user,
        subscription_plan=plan,
        stripe_subscription_id=request.session.get("subscription"),
        start_date=now(),
        end_date=now() + timedelta(days=30),
        status=True,
    )

    # Link the subscription to the UserProfile
    user_profile = request.user.userprofile
    user_profile.subscription = subscription
    user_profile.save()

    # Clean up session data
    request.session.pop("selected_plan_id", None)
    request.session.pop("stripe_checkout_url", None)
    request.session.pop("stripe_checkout_session_id", None)

    messages.success(request, f"Your subscription to {plan.name} is active! 🎉")
    return redirect("user_profile")


@login_required
def user_profile(request):
    """User profile page displaying subscriptions"""
    user_profile = request.user.userprofile
    subscription = user_profile.subscription

    # Determine subscription status
    if subscription:
        # Fetch latest status from Stripe
        stripe_subscription = None
        if subscription.stripe_subscription_id:
            try:
                stripe_subscription = stripe.Subscription.retrieve(
                    subscription.stripe_subscription_id
                )
            except stripe.error.StripeError as e:
                logger.error(f"Error retrieving subscription from Stripe: {e}")

        # Determine if the subscription is still active or pending cancellation
        if subscription.status and stripe_subscription:
            if stripe_subscription.cancel_at_period_end:
                subscription_status = "Pending Cancellation"
            else:
                subscription_status = "Active"
        elif subscription.end_date and subscription.end_date > now():
            subscription_status = "Pending Cancellation"
        else:
            subscription_status = "Expired"

        # Save the updated status in case the subscription is newly marked
        subscription.save()
    else:
        subscription_status = "No Subscription"

        borrowed_sets = Borrowing.objects.filter(
            user=request.user, is_returned=False
        )

        notifications = Notification.objects.filter(
            user=request.user
        ).order_by('-created_at')[:5]

    return render(request, 'home/user_profile.html', {
        'user_profile': user_profile,
        'subscription': subscription,
        'subscription_status': subscription_status,
        'borrowed_sets': borrowed_sets,
        'notifications': notifications,
        'emailaddresses': emailaddresses,
    })


@login_required
def return_borrowed_sets(request):
    """Allows users to return borrowed LEGO sets and notifies admin."""
    if request.method == "POST":
        returned_set_ids = request.POST.getlist('return_sets')

        if returned_set_ids:
            returned_sets = Borrowing.objects.filter(
                id__in=returned_set_ids, user=request.user
            )

            returned_set_names = [] #Store returned set names for email

            for borrow in returned_sets:
                borrow.is_returned = True  # Mark as returned
                borrow.save()

                # Increase stock when a set is returned
                borrow.lego_set.stock += 1  # Add back to stock
                borrow.lego_set.is_borrowed = False  # Set as available
                borrow.lego_set.save()

                # **Create Notification for Returning a Set**
                Notification.objects.create(
                    user=request.user,
                    message=f"{request.user.username} returned {borrow.lego_set.name}.",
                    category="borrowing"
                )

            messages.success(
                request, "Selected LEGO set(s) have been returned!"
            )

            #Send Return Confirmation Email
            subject = "LEGO Set Return Confirmation - Brick Heroes"
            context = {
                'user': request.user,
                'returned_sets': returned_set_names,
            }
            email_html_message = render_to_string(
                'allauth/account/borrow_return_confirmation.html', context
            )
            email_plain_message = strip_tags(email_html_message)

            send_mail(
                subject=subject,
                message=email_plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[request.user.email],
                html_message=email_html_message,
                fail_silently=False,
            )

        else:
            messages.warning(
                request, "Please select at least one LEGO set to return."
            )

    return redirect('user_profile')  # Redirect back to profile after return
