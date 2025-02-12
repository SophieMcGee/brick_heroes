from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from subscriptions.models import (
    SubscriptionPlan, Subscription, Borrowing, UserProfile
)
from datetime import timedelta
from django.utils.timezone import now
from django.contrib import admin
from subscriptions.admin import (
    SubscriptionAdmin, SubscriptionPlanAdmin,
    BorrowingAdmin, UserProfileAdmin
)


class TestSubscriptionModels(TestCase):

    def setUp(self):
        """Create test user, subscription plan, and subscription"""
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.plan = SubscriptionPlan.objects.create(
            name="Tier 1", price=9.99, max_active_borrows=1
        )

        # Create a single subscription plan
        self.subscription_plan = SubscriptionPlan.objects.create(
            name="Tier 1",
            price=9.99,
            max_active_borrows=1
        )

        # Create a subscription linked to the user and plan
        self.subscription = Subscription.objects.create(
            user=self.user,
            stripe_subscription_id="test_sub_123",
            status=True,
            subscription_plan=self.subscription_plan
        )

        # Assign the subscription to the user's profile correctly
        self.user.userprofile.subscription = self.subscription
        self.user.userprofile.save()

    def test_subscription_plan_str(self):
        """Ensure SubscriptionPlan string representation is correct"""
        self.assertEqual(str(self.plan), "Tier 1")

    def test_subscription_str(self):
        """Ensure Subscription string representation includes user and plan"""
        self.assertEqual(str(self.subscription), "testuser - Tier 1 (Active)")

    def test_subscription_expiration_check(self):
        """Ensure expired subscriptions are marked as inactive"""
        self.subscription.end_date = now() - timedelta(days=1)
        self.subscription.save()
        Subscription.check_expired_subscriptions()
        self.subscription.refresh_from_db()
        self.assertFalse(
            self.subscription.status, "Expired subs should be inactive"
        )

    def test_renew_subscription(self):
        """Ensure renewing a subscription updates the end date"""
        self.subscription.renew_subscription()
        self.subscription.refresh_from_db()
        self.assertTrue(self.subscription.status)
        self.assertEqual(
            self.subscription.end_date.date(), (now() + timedelta(days=30)).date()
        )


class TestBorrowingModel(TestCase):

    def setUp(self):
        """Create test user and product"""
        self.user = User.objects.create_user(
            username='testuser', password='password123'
        )
        self.plan = SubscriptionPlan.objects.create(
            name="Tier 1", price=9.99, max_active_borrows=1
        )
        self.subscription = Subscription.objects.create(
            user=self.user,
            subscription_plan=self.plan,
            start_date=now(),
            end_date=now() + timedelta(days=30),
            status=True
        )
        self.borrowing = Borrowing.objects.create(
            user=self.user,
            subscription=self.subscription,
            lego_set=None,
            borrowed_on=now(),
            is_returned=False
        )

    def test_borrowing_valid(self):
        """Ensure a valid borrowing record can be created"""
        self.assertFalse(self.borrowing.is_returned)
        self.borrowing.is_returned = True
        self.borrowing.save()
        self.assertTrue(self.borrowing.is_returned)


class TestSubscriptionViews(TestCase):

    def setUp(self):
        """Set up user, subscription plan, and active subscription"""
        self.user = User.objects.create_user(
            username='testuser', password='password123'
        )
        self.plan = SubscriptionPlan.objects.create(
            name="Tier 1", price=9.99, max_active_borrows=1
        )
        self.subscription = Subscription.objects.create(
            user=self.user,
            subscription_plan=self.plan,
            start_date=now(),
            end_date=now() + timedelta(days=30),
            status=True
        )
        self.client.login(username='testuser', password='password123')

    def test_subscription_plans_view(self):
        """Ensure subscription plans page loads correctly"""
        response = self.client.get(reverse('subscription_plans'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'subscriptions/subscription_plans.html'
        )

    def test_subscription_confirmation_view(self):
        """Ensure subscription confirmation page loads correctly"""
        # Create a test subscription plan (needed for the URL)
        plan = SubscriptionPlan.objects.create(
            name="Tier 1", price=9.99, max_active_borrows=1
        )

        # Simulate a session variable for Stripe checkout URL
        session = self.client.session
        session["stripe_checkout_url"] = "https://checkout.stripe.com/test_url"
        session.save()

        response = self.client.get(
            reverse("subscription_confirmation", args=[plan.id])
        )

        # Ensure the response is 200 OK
        self.assertEqual(response.status_code, 200)

    def test_subscription_success_view(self):
        """Ensure subscription success page loads and redirects"""
        response = self.client.get(reverse("subscription_success"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("user_profile"))

    def test_cancel_subscription_view(self):
        """Ensure users can cancel subscriptions"""
        response = self.client.post(reverse('cancel_subscription'))
        self.assertIn(response.status_code, [200, 302])
        self.subscription.refresh_from_db()
        self.assertTrue(
            self.subscription.status, "Sub should be active until expiry"
        )


class TestAdminPanel(TestCase):

    def setUp(self):
        """Set up test data for admin tests"""
        self.user = User.objects.create_superuser(
            username='admin', password='adminpass'
        )
        self.client.login(username='admin', password='adminpass')

        self.plan = SubscriptionPlan.objects.create(
            name="Tier 1", price=9.99, max_active_borrows=1
        )
        self.subscription = Subscription.objects.create(
            user=self.user,
            subscription_plan=self.plan,
            start_date=now(),
            end_date=now() + timedelta(days=30),
            status=True
        )

    def test_subscription_admin_registered(self):
        """Ensure Subscription model is registered in admin"""
        self.assertTrue(admin.site.is_registered(Subscription))

    def test_subscription_plan_admin_registered(self):
        """Ensure SubscriptionPlan model is registered in admin"""
        self.assertTrue(admin.site.is_registered(SubscriptionPlan))

    def test_admin_subscription_list_display(self):
        """Ensure SubscriptionAdmin displays the correct fields"""
        model_admin = SubscriptionAdmin(Subscription, admin.site)
        self.assertEqual(
            model_admin.list_display,
            ('user', 'subscription_plan', 'start_date', 'end_date', 'status')
        )

    def test_admin_subscription_plan_list_display(self):
        """Ensure SubscriptionPlanAdmin displays correct fields"""
        model_admin = SubscriptionPlanAdmin(SubscriptionPlan, admin.site)
        self.assertEqual(
            model_admin.list_display,
            ('name', 'price', 'max_active_borrows', 'stripe_price_id')
        )


class TestUserProfileModel(TestCase):

    def setUp(self):
        """Create a user, subscription, and borrowed LEGO sets"""
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.plan = SubscriptionPlan.objects.create(
            name="Tier 1", price=9.99, max_active_borrows=1
            )

        # Create an active subscription
        self.subscription = Subscription.objects.create(
            user=self.user,
            subscription_plan=self.plan,
            stripe_subscription_id="test_sub_123",
            status=True
        )

        # Assign subscription to UserProfile
        self.user_profile = UserProfile.objects.get(user=self.user)
        self.user_profile.subscription = self.subscription
        self.user_profile.save()

        Borrowing.objects.create(
            user=self.user,
            subscription=self.subscription,
            is_returned=False
        )

    def test_user_profile_str(self):
        """Ensure UserProfile string representation is correct"""
        self.assertEqual(str(self.user_profile), "testuser")

    def test_user_profile_can_borrow(self):
        """Ensure the borrowing limit is respected"""
        self.plan = SubscriptionPlan.objects.create(
            name="Tier 1", price=9.99, max_active_borrows=2
        )
        self.subscription = Subscription.objects.create(
            user=self.user,
            subscription_plan=self.plan,
            start_date=now(),
            end_date=now() + timedelta(days=30),
            status=True
        )
        self.user_profile.subscription = self.subscription
        self.user_profile.save()

        # Should allow borrowing since the limit is 2
        self.assertTrue(self.user_profile.can_borrow())

        # Create another borrowing record to reach the limit
        Borrowing.objects.create(
            user=self.user,
            subscription=self.subscription,
            lego_set=None,
            borrowed_on=now(),
            is_returned=False
        )

        self.assertFalse(
            self.user_profile.can_borrow(),
            "User should not be able to borrow more than allowed"
        )


if __name__ == '__main__':
    TestCase.main()
