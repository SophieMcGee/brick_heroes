from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.timezone import now
from cart.models import (
    Cart, CartItem, BorrowOrder, BorrowOrderItem
)
from products.models import Product, Category
from subscriptions.models import (
    Subscription, SubscriptionPlan, UserProfile, Borrowing
)
from cart.forms import DeliveryInfoForm


class TestCartModel(TestCase):

    def setUp(self):
        """Create a test user and cart"""
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.cart = Cart.objects.create(user=self.user)

    def test_cart_str(self):
        """Ensure string representation of Cart is correct"""
        self.assertEqual(str(self.cart), f"Cart of {self.user.username}")


class TestCartItemModel(TestCase):

    def setUp(self):
        """Create test data for CartItem"""
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.cart = Cart.objects.create(user=self.user)
        self.category = Category.objects.create(
            name="City", friendly_name="LEGO City"
        )
        self.product = Product.objects.create(
            name="LEGO Fire Truck", category=self.category, stock=10
        )
        self.cart_item = CartItem.objects.create(
            cart=self.cart, product=self.product
        )

    def test_cart_item_str(self):
        """Ensure string representation of CartItem is correct"""
        self.assertEqual(
            str(self.cart_item),
            f"{self.product.name} (Borrowed by {self.cart.user.username})"
        )


class TestBorrowOrderModel(TestCase):

    def setUp(self):
        """Create test data for BorrowOrder"""
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.order = BorrowOrder.objects.create(
            user=self.user,
            full_name="John Doe",
            address_line1="123 Brick Street",
            city="Blocktown",
            postal_code="12345",
            country="Brickland",
            status="Pending"
        )

    def test_borrow_order_str(self):
        """Ensure string representation of BorrowOrder is correct"""
        self.assertEqual(
            str(self.order),
            f"Order {self.order.id} for {self.user.username}"
        )


class TestCartViews(TestCase):

    def setUp(self):
        """Set up test data for cart views"""
        self.user = User.objects.create_user(
            username="testuser", password="password"
        )
        self.client.login(username="testuser", password="password")

        self.subscription_plan = SubscriptionPlan.objects.create(
            name="Tier 1",
            price=9.99,
            max_active_borrows=1
        )

        self.subscription = Subscription.objects.create(
            user=self.user,
            stripe_subscription_id="test_sub_123",
            status=True,
            subscription_plan=self.subscription_plan
        )

        self.user.userprofile.subscription = self.subscription
        self.user.userprofile.save()

        self.product = Product.objects.create(
            name="Test LEGO Set",
            description="A test LEGO set",
            stock=5,
        )
        self.cart = Cart.objects.create(user=self.user)

    def test_view_cart(self):
        """Ensure cart page loads successfully"""
        response = self.client.get(reverse("shopping_cart"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "cart/shopping_cart.html")

    def test_remove_from_cart(self):
        """Ensure users can remove items from the borrow cart"""
        cart_item = CartItem.objects.create(
            cart=self.cart, product=self.product
        )
        response = self.client.post(
            reverse("remove_from_cart", args=[cart_item.id])
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(CartItem.objects.filter(id=cart_item.id).exists())

    def test_checkout_view(self):
        """Ensure checkout page loads successfully"""
        self.client.login(username="testuser", password="password123")

        category = Category.objects.create(
            name="City", friendly_name="LEGO City"
        )
        product = Product.objects.create(
            name="LEGO Fire Truck",
            category=category,
            stock=10,
            sku="fire-truck-001"
        )

        cart_item = CartItem.objects.create(cart=self.cart, product=product)

        plan = SubscriptionPlan.objects.create(
            name="Tier 1", price=9.99, max_active_borrows=2
        )
        subscription = Subscription.objects.create(
            user=self.user,
            subscription_plan=plan,
            status=True
        )
        self.user.userprofile.subscription = subscription
        self.user.userprofile.save()

        response = self.client.get(reverse("checkout"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "cart/checkout.html")


class TestDeliveryInfoForm(TestCase):

    def test_valid_delivery_form(self):
        """Ensure valid delivery information form passes validation"""
        form_data = {
            'full_name': "John Doe",
            'address_line1': "123 Brick Street",
            'city': "Blocktown",
            'postal_code': "12345",
            'country': "Brickland"
        }
        form = DeliveryInfoForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_delivery_form(self):
        """Ensure missing required fields fail validation"""
        form_data = {
            'full_name': "",
            'address_line1': "123 Brick Street",
            'city': "Blocktown",
            'postal_code': "",
            'country': "Brickland"
        }
        form = DeliveryInfoForm(data=form_data)
        self.assertFalse(form.is_valid())
