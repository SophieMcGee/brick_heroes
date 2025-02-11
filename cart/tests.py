from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from cart.models import Borrowing
from products.models import Product
from django.contrib.auth.models import User
from products.models import Product
from datetime import date


class TestBorrowingModel(TestCase):

    def setUp(self):
        """Create test user and product"""
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.product = Product.objects.create(
            name="LEGO Star Wars", stock=5
        )

    def test_borrowing_valid(self):
        """Ensure a valid borrowing record can be created"""
        borrow = Borrowing.objects.create(
            user=self.user,
            lego_set=self.product,
            borrowed_on=date.today(),
            is_returned=False
        )
        self.assertEqual(borrow.lego_set.name, "LEGO Star Wars")

class TestCartViews(TestCase):

    def setUp(self):
        """Set up test user, product, and borrowing cart"""
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.product = Product.objects.create(name="LEGO Batman", stock=3)
        self.borrow = Borrowing.objects.create(
            user=self.user,
            lego_set=self.product,
            borrowed_on=date.today(),
            is_returned=False
        )
        self.client.login(username='testuser', password='password123')

    def test_cart_view(self):
        """Ensure the cart page loads correctly"""
        response = self.client.get(reverse('view_cart'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart/cart.html')

    def test_checkout_view(self):
        """Ensure checkout page loads correctly"""
        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart/checkout.html')
