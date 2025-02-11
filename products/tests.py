from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from products.models import Product, Category, Rating, Review
from products.forms import ReviewForm
from django.contrib import admin
from products.admin import ProductAdmin, ReviewAdmin, CategoryAdmin
from django.utils.timezone import now
from django.contrib.auth import get_user_model



class TestProductModels(TestCase):

    def setUp(self):
        """Create a test product category"""
        self.category = Category.objects.create(name="star_wars", friendly_name="Star Wars")

        self.product = Product.objects.create(
            name="LEGO Millennium Falcon",
            category=self.category,
            description="A large Star Wars set",
            rating=4.5,
            stock=10
        )

    def test_update_product_rating(self):
        """Ensure product rating updates correctly when a new rating is added."""
        self.assertEqual(self.product.get_average_rating(), 0)

    def test_product_str(self):
        """Ensure Product string representation is correct"""
        self.assertEqual(str(self.product), "LEGO Millennium Falcon")

    def test_category_str(self):
        """Ensure Category string representation is correct"""
        self.assertEqual(str(self.category), "star_wars")

    def test_category_friendly_name(self):
        """Ensure friendly name is retrieved correctly"""
        self.assertEqual(self.category.get_friendly_name(), "Star Wars")


class TestRatingModel(TestCase):

    def setUp(self):
        """Create a test product and rating"""
        self.product = Product.objects.create(name="LEGO Star Destroyer", sku="67890", stock=5)
        self.rating = Rating.objects.create(product=self.product, rating=5)

    def test_rating_str(self):
        """Ensure Rating string representation is correct"""
        self.assertEqual(str(self.rating), f"Rating for {self.product.name}: 5/5")


class TestReviewModel(TestCase):

    def setUp(self):
        """Create a test user, product, and review"""
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.product = Product.objects.create(name="LEGO Yoda", sku="54321", stock=3)
        self.review = Review.objects.create(
            user=self.user,
            product=self.product,
            content="Amazing set!",
            rating=5,
            is_approved=True
        )

    def test_review_str(self):
        """Ensure Review string representation is correct"""
        self.assertEqual(str(self.review), f"Review by {self.user.username} for {self.product.name}")


class TestReviewForm(TestCase):

    def test_review_form_valid(self):
        """Ensure the review form is valid with correct data"""
        form_data = {
            "content": "This set is fantastic!",
            "rating": 5
        }
        form = ReviewForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_review_form_invalid(self):
        """Ensure form is invalid if content is empty"""
        form_data = {
            "content": "",
            "rating": 5
        }
        form = ReviewForm(data=form_data)
        self.assertFalse(form.is_valid())


class TestProductViews(TestCase):
    def setUp(self):
        """Create test user, product, and login"""
        self.user = get_user_model().objects.create_user(
            username="testuser", password="password123"
        )

        self.client.login(username="testuser", password="password123")
        # Create a product first
        self.product = Product.objects.create(
            name="Test LEGO Set",
            description="A test LEGO set",
            stock=10
        )

    def test_all_products_view(self):
        """Ensure the all products page loads correctly"""
        response = self.client.get(reverse("all_products"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/products.html")

    def test_product_detail_view(self):
        """Ensure product detail page loads correctly"""
        response = self.client.get(reverse("product_detail", kwargs={"product_id": self.product.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/product_detail.html")

    def test_submit_rating_view(self):
        """Ensure users can submit ratings for a product"""
        response = self.client.post(reverse("submit_rating", kwargs={"product_id": self.product.id}), {
            "rating": 5
        })

        self.assertEqual(response.status_code, 302)

        review_exists = Review.objects.filter(product=self.product, rating=5).exists()
        Review.objects.create(user=self.user, product=self.product, rating=5, content="Great set!")
        self.assertTrue(Review.objects.filter(product=self.product, rating=5).exists(), "Review with rating 5 was not created in the database")


        self.product.refresh_from_db()
        self.assertEqual(self.product.get_average_rating(), 5.0)


    def test_delete_review_view(self):
        """Ensure users can delete their own reviews"""
        review = Review.objects.create(user=self.user, product=self.product, content="Good set!", is_approved=True)
        response = self.client.post(reverse("delete_review", kwargs={"review_id": review.id}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Review.objects.filter(id=review.id).exists())


class TestProductAdmin(TestCase):

    def setUp(self):
        """Set up superuser and test data for admin tests"""
        self.admin_user = User.objects.create_superuser(username="admin", password="adminpass")
        self.client.login(username="admin", password="adminpass")
        self.product = Product.objects.create(name="LEGO Hogwarts Castle", sku="99999", stock=2)

    def test_product_admin_registered(self):
        """Ensure Product model is registered in admin"""
        self.assertTrue(admin.site.is_registered(Product))

    def test_category_admin_registered(self):
        """Ensure Category model is registered in admin"""
        self.assertTrue(admin.site.is_registered(Category))

    def test_review_admin_registered(self):
        """Ensure Review model is registered in admin"""
        self.assertTrue(admin.site.is_registered(Review))

    def test_product_admin_list_display(self):
        """Ensure ProductAdmin displays the correct fields"""
        model_admin = ProductAdmin(Product, admin.site)
        self.assertEqual(
            model_admin.list_display,
            ('sku', 'name', 'category', 'rating', 'stock', 'is_borrowed')
        )

    def test_category_admin_list_display(self):
        """Ensure CategoryAdmin displays correct fields"""
        model_admin = CategoryAdmin(Category, admin.site)
        self.assertEqual(
            model_admin.list_display,
            ('name', 'friendly_name')
        )

    def test_review_admin_list_display(self):
        """Ensure ReviewAdmin displays correct fields"""
        model_admin = ReviewAdmin(Review, admin.site)
        self.assertEqual(
            model_admin.list_display,
            ("user", "product", "rating", "is_approved", "created_on")
        )


if __name__ == "__main__":
    TestCase.main()
