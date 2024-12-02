from django.test import TestCase, Client
from django.urls import reverse
from django.utils.timezone import now, timedelta
from products.models import Product
from django.db.models import Sum
from unittest.mock import patch


class HomeViewTests(TestCase):
    def setUp(self):
        """Set up test data for the homepage view."""
        self.client = Client()
        self.home_url = reverse("home")
        self.thirty_days_ago = now() - timedelta(days=30)

        # Create sample products
        for i in range(6):
            Product.objects.create(
                name=f"Product {i}",
                gender=random.choice(["M", "W"]),
                is_active=True,
                created_at=now() if i < 4 else self.thirty_days_ago - timedelta(days=1),
                rating=random.randint(1, 5) if i < 4 else None,
            )

        # Add sales data for revenue
        for product in Product.objects.all():
            product.sales_data.create(revenue_generated=random.randint(100, 1000))

    def test_homepage_renders_correctly(self):
        """Test that the homepage renders correctly."""
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/index.html")
        self.assertIn("meta_description", response.context)

    def test_new_in_products(self):
        """Test that 'New In' section contains the correct products."""
        response = self.client.get(self.home_url)
        new_in_products = Product.objects.filter(
            created_at__gte=self.thirty_days_ago, is_active=True
        ).order_by("-created_at")[:4]
        self.assertQuerysetEqual(
            response.context["new_in_products"],
            new_in_products,
            transform=lambda x: x,
        )

    def test_for_him_products(self):
        """Test that 'For Him' section contains the correct products."""
        response = self.client.get(self.home_url)
        for_him_products = Product.objects.filter(
            gender="M", is_active=True
        ).order_by("-created_at")[:4]
        self.assertQuerysetEqual(
            response.context["for_him_products"],
            for_him_products,
            transform=lambda x: x,
        )

    def test_for_her_products(self):
        """Test that 'For Her' section contains the correct products."""
        response = self.client.get(self.home_url)
        for_her_products = Product.objects.filter(
            gender="W", is_active=True
        ).order_by("-created_at")[:4]
        self.assertQuerysetEqual(
            response.context["for_her_products"],
            for_her_products,
            transform=lambda x: x,
        )

    def test_most_popular_products(self):
        """Test that 'Most Popular' section contains the correct products."""
        response = self.client.get(self.home_url)
        most_popular_products = Product.objects.annotate(
            total_revenue=Sum("sales_data__revenue_generated")
        ).order_by("-total_revenue")[:4]
        self.assertQuerysetEqual(
            response.context["most_popular_products"],
            most_popular_products,
            transform=lambda x: x,
        )

    def test_highest_rated_products(self):
        """Test that 'Highest Rated' section contains the correct products."""
        response = self.client.get(self.home_url)
        highest_rated_products = Product.objects.filter(
            rating__isnull=False, is_active=True
        ).order_by("-rating")[:4]
        self.assertQuerysetEqual(
            response.context["highest_rated_products"],
            highest_rated_products,
            transform=lambda x: x,
        )

    @patch("random.sample")
    def test_random_products(self, mock_random_sample):
        """Test that 'Random Products' section contains random products."""
        all_active_products = Product.objects.filter(is_active=True)
        mock_random_sample.return_value = list(all_active_products[:4])
        response = self.client.get(self.home_url)
        self.assertEqual(
            response.context["random_products"], list(all_active_products[:4])
        )

    def test_meta_description_in_context(self):
        """Test that the meta description is present in the context."""
        response = self.client.get(self.home_url)
        self.assertIn(
            "meta_description",
            response.context,
        )
        self.assertTrue(
            "Welcome to Maison Lavaux" in response.context["meta_description"]
        )
