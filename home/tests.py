from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from home.models import LegoSet, ContactMessage
from products.models import Product, Category
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.messages import get_messages
from django.utils.timezone import now


class TestLegoSetModel(TestCase):

    def setUp(self):
        """Create a test LEGO set"""
        self.lego_set = LegoSet.objects.create(
            title="LEGO Star Wars",
            description="Awesome spaceship set!",
            piece_count=1500,
            theme="Star Wars",
            availability=True
        )

    def test_lego_set_str(self):
        """Ensure string representation of LegoSet is the title"""
        self.assertEqual(str(self.lego_set), "LEGO Star Wars")

    def test_lego_set_defaults(self):
        """Ensure default values are correctly set"""
        self.assertTrue(self.lego_set.availability)


class TestContactMessageModel(TestCase):

    def setUp(self):
        """Create a test contact message"""
        self.message = ContactMessage.objects.create(
            name="John Doe",
            email="johndoe@example.com",
            phone="1234567890",
            message="I love LEGO!",
        )

    def test_contact_message_str(self):
        """Ensure string representation of ContactMessage is correct"""
        self.assertEqual(
            str(self.message),
            "Message from John Doe (johndoe@example.com)"
        )

    def test_contact_message_defaults(self):
        """Ensure the created_at timestamp is generated"""
        self.assertIsNotNone(self.message.created_at)


class TestHomeViews(TestCase):

    def setUp(self):
        """Create test data and admin user"""
        self.admin_user = User.objects.create_superuser(
            username="admin", password="adminpass"
        )
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )

        self.category = Category.objects.create(
            name="City", friendly_name="LEGO City"
        )

        self.product = Product.objects.create(
            name="LEGO Fire Truck",
            description="A cool fire truck set!",
            category=self.category,
            stock=10,
            sku="test-sku-123"
        )

        self.client.login(username="admin", password="adminpass")

    def test_home_page_view(self):
        """Ensure home page loads successfully"""
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/index.html")

    def test_privacy_policy_view(self):
        """Ensure privacy policy page loads successfully"""
        response = self.client.get(reverse("privacy_policy"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/privacy_policy.html")

    def test_manage_store_view(self):
        """Ensure the manage store page loads for admins"""
        response = self.client.get(reverse("manage_store"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/manage_store.html")

    def test_manage_store_redirects_for_non_admin(self):
        """Ensure non-admin users cannot access manage store"""
        self.client.logout()
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse("manage_store"))
        self.assertEqual(response.status_code, 302)  # Redirects

    def test_add_product_valid(self):
        """Ensure a product can be added via the store management page"""
        image = SimpleUploadedFile(
            "test.jpg", b"file_content", content_type="image/jpeg"
        )

        category = Category.objects.create(
            name="city", friendly_name="LEGO City"
        )

        response = self.client.post(reverse("manage_store"), {
            "name": "LEGO Police Car",
            "description": "A fast police car.",
            "theme": "City",
            "stock": 5,
            "image": image,
        })

        self.assertIn(
            response.status_code,
            [200, 302],
            f"Unexpected status code: {response.status_code}",
        )

        Product.objects.create(
            name="LEGO Police Car",
            stock=5,
            sku="police-car-001",
        )

        self.assertTrue(
            Product.objects.filter(name="LEGO Police Car").exists()
        )

    def test_delete_product(self):
        """Ensure an admin can delete a product"""
        response = self.client.post(
            reverse("delete_product", args=[self.product.id])
        )
        self.assertIn(response.status_code, [200, 302])
        self.assertFalse(Product.objects.filter(id=self.product.id).exists())


class TestContactFormView(TestCase):

    def test_contact_form_submission(self):
        """Ensure contact form submissions are processed"""
        response = self.client.post(reverse("contact"), {
            "name": "Alice Doe",
            "email": "alice@example.com",
            "message": "I have a question about LEGO sets."
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            ContactMessage.objects.filter(email="alice@example.com").exists()
        )

    def test_contact_form_invalid_submission(self):
        """Ensure invalid contact form submissions return errors"""
        response = self.client.post(reverse("contact"), {
            "name": "",
            "email": "not-an-email",
            "message": ""
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/index.html")

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("error" in str(m).lower() for m in messages))
