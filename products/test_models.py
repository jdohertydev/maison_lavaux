from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from products.models import Category, Product, Review

class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Fragrances",
            friendly_name="Luxury Fragrances"
        )

    def test_category_str(self):
        self.assertEqual(str(self.category), "Fragrances")

    def test_get_friendly_name(self):
        self.assertEqual(self.category.get_friendly_name(), "Luxury Fragrances")


class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Fragrances")
        self.product = Product.objects.create(
            category=self.category,
            sku="12345",
            name="Luxury Perfume",
            gender="U",
            description="A premium unisex fragrance.",
            price=100.00,
            discount_price=90.00,
            stock_quantity=50,
            size="50ml"
        )

    def test_product_str(self):
        self.assertEqual(str(self.product), "Luxury Perfume")

    def test_discount_price_validation(self):
        self.product.discount_price = 110.00
        with self.assertRaises(ValidationError):
            self.product.clean()

    def test_update_rating(self):
        user1 = User.objects.create_user(username="user1", password="password")
        user2 = User.objects.create_user(username="user2", password="password")
        Review.objects.create(product=self.product, user=user1, rating=5)
        Review.objects.create(product=self.product, user=user2, rating=4)

        self.product.update_rating()
        self.assertEqual(self.product.rating, 4.5)

    def test_default_gender(self):
        self.assertEqual(self.product.gender, "U")


class ReviewModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user1", password="password")
        self.category = Category.objects.create(name="Fragrances")
        self.product = Product.objects.create(
            category=self.category,
            name="Luxury Perfume",
            price=100.00
        )
        self.review = Review.objects.create(
            product=self.product,
            user=self.user,
            rating=5,
            comment="Amazing scent!"
        )

    def test_review_str(self):
        self.assertEqual(
            str(self.review),
            f"Review by {self.user.username} for {self.product.name} (5/5)"
        )

    def test_unique_review_per_user_product(self):
        with self.assertRaises(Exception):
            Review.objects.create(
                product=self.product,
                user=self.user,
                rating=4,
                comment="Great value!"
            )
