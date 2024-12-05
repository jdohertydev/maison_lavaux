from django.test import TestCase
from django.contrib.sitemaps import Sitemap
from django.utils.timezone import now, timedelta
from products.models import Product
from ..sitemaps import ProductSitemap


class ProductSitemapTests(TestCase):
    def setUp(self):
        """Set up test data for the ProductSitemap."""
        # Create sample products
        self.product1 = Product.objects.create(
            name="Product 1",
            updated=now() - timedelta(days=1),
        )
        self.product2 = Product.objects.create(
            name="Product 2",
            updated=now() - timedelta(days=2),
        )
        self.sitemap = ProductSitemap()

    def test_sitemap_items(self):
        """Test that the sitemap returns all products."""
        items = self.sitemap.items()
        self.assertIn(self.product1, items)
        self.assertIn(self.product2, items)
        self.assertEqual(len(items), Product.objects.count())

    def test_sitemap_lastmod(self):
        """Test that the lastmod method returns the correct updated time."""
        self.assertEqual(
            self.sitemap.lastmod(self.product1), self.product1.updated
        )
        self.assertEqual(
            self.sitemap.lastmod(self.product2), self.product2.updated
        )

    def test_sitemap_priority(self):
        """Test that the priority is set correctly."""
        self.assertEqual(self.sitemap.priority, 0.8)

    def test_sitemap_changefreq(self):
        """Test that the changefreq is set correctly."""
        self.assertEqual(self.sitemap.changefreq, "weekly")

    def test_sitemap_lastmod_none(self):
        """Test that lastmod returns None if 'updated' field is absent."""
        product = Product.objects.create(
            name="Product 3"
        )  # No 'updated' field
        self.assertIsNone(self.sitemap.lastmod(product))
