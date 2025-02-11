from django.test import TestCase
from subscriptions.forms import SubscriptionForm
from django.urls import reverse
from django.contrib.auth.models import User
from subscriptions.models import SubscriptionPlan, Subscription
from django.contrib.auth.models import User
from datetime import date


class TestSubscriptionForm(TestCase):
    
    def setUp(self):
        """Create a test user and subscription plan"""
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.plan = SubscriptionPlan.objects.create(
            name="Tier 1", price=9.99, max_active_borrows=1
        )

    def test_valid_subscription_form(self):
        """Ensure a subscription form with valid data is accepted"""
        form_data = {
            'user': self.user.id,
            'subscription_plan': self.plan.id,
            'start_date': date.today(),
            'end_date': date.today(),
            'status': 'active'
        }
        form = SubscriptionForm(data=form_data)
        self.assertTrue(form.is_valid(), msg="Subscription form should be valid")

    def test_subscription_form_invalid_date(self):
        """Ensure form fails when end_date is before start_date"""
        form_data = {
            'user': self.user.id,
            'subscription_plan': self.plan.id,
            'start_date': date.today(),
            'end_date': date.today().replace(day=date.today().day - 1),
            'status': 'active'
        }
        form = SubscriptionForm(data=form_data)
        self.assertFalse(form.is_valid(), msg="Form should be invalid if end_date is before start_date")

    class TestSubscriptionViews(TestCase):

    def setUp(self):
        """Set up user, subscription plan, and active subscription"""
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.plan = SubscriptionPlan.objects.create(name="Tier 1", price=9.99, max_active_borrows=1)
        self.subscription = Subscription.objects.create(
            user=self.user,
            subscription_plan=self.plan,
            start_date=date.today(),
            end_date=date.today().replace(day=date.today().day + 30),
            status="active"
        )
        self.client.login(username='testuser', password='password123')

    def test_subscription_plans_view(self):
        """Ensure subscription plans page loads correctly"""
        response = self.client.get(reverse('subscription_plans'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'subscriptions/subscription_plans.html')

    def test_subscription_success_view(self):
        """Ensure subscription success page loads"""
        response = self.client.get(reverse('subscription_success'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'subscriptions/subscription_success.html')

    def test_cancel_subscription_view(self):
        """Ensure users can cancel subscriptions"""
        response = self.client.post(reverse('cancel_subscription'))
        self.assertEqual(response.status_code, 302)
        self.subscription.refresh_from_db()
        self.assertEqual(self.subscription.status, "cancelled")
