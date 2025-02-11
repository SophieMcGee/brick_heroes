from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from notifications.models import Notification
from products.models import Review, Product
from django.utils.timezone import now


class TestNotificationModel(TestCase):

    def setUp(self):
        """Create a test user and notification"""
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.notification = Notification.objects.create(
            user=self.user,
            message="Your subscription has been renewed!",
            category="subscription",
            is_read=False
        )

    def test_notification_str(self):
        """Ensure the string representation of Notification is correct"""
        self.assertEqual(str(self.notification), "subscription - Your subscription has been renewed!")

    def test_mark_notification_as_read(self):
        """Ensure notification read status updates correctly"""
        self.notification.is_read = True
        self.notification.save()
        self.assertTrue(self.notification.is_read)


class TestNotificationViews(TestCase):

    def setUp(self):
        """Create test user, admin, and notifications"""
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.admin = User.objects.create_superuser(username="admin", password="adminpass")

        self.notification = Notification.objects.create(
            user=self.user,
            message="Lego set is available for borrowing.",
            category="borrowing"
        )

        self.client.login(username="testuser", password="password123")

    def test_admin_notifications_view(self):
        """Ensure admin notifications page loads correctly"""
        self.client.login(username="adminuser", password="password")  # Make sure an admin is logged in

        response = self.client.get(reverse("admin_notifications"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/admin_notifications.html")

    def test_admin_notifications_view(self):
        """Ensure admin notifications page loads correctly"""
        self.client.logout()
        self.client.login(username="admin", password="adminpass")

        response = self.client.get(reverse("admin_notifications"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "notifications/admin_notifications.html")

    def test_delete_notification_view(self):
        """Ensure admins can delete notifications"""
        self.client.logout()
        self.client.login(username="admin", password="adminpass")

        response = self.client.post(reverse("delete_notification", kwargs={"notification_id": self.notification.id}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Notification.objects.filter(id=self.notification.id).exists())


class TestReviewApproval(TestCase):

    def setUp(self):
        """Create test user, admin, product, and review"""
        self.admin = User.objects.create_superuser(username="admin", password="adminpass")
        self.user = User.objects.create_user(username="testuser", password="password123")

        self.product = Product.objects.create(
            name="Test LEGO Set",
            description="A test LEGO set",
            stock=10
        )

        self.review = Review.objects.create(
            user=self.user,
            product=self.product,
            content="This is a great set!",
            is_approved=False
        )

        self.client.login(username="admin", password="adminpass")

    def test_approve_review_view(self):
        """Ensure admins can approve a review"""
        response = self.client.post(reverse("approve_review", kwargs={"review_id": self.review.id}))
        self.assertEqual(response.status_code, 302)
        self.review.refresh_from_db()
        self.assertTrue(self.review.is_approved)
