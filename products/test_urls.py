from django.test import SimpleTestCase
from django.urls import reverse, resolve
from products import views


class TestProductUrls(SimpleTestCase):

    def test_products_url_resolves(self):
        """Test the URL for all products resolves correctly."""
        url = reverse("products")
        self.assertEqual(resolve(url).func, views.all_products)

    def test_product_detail_url_resolves(self):
        """Test the product detail URL resolves correctly."""
        url = reverse("product_detail", args=[1])
        self.assertEqual(resolve(url).func, views.product_detail)

    def test_add_review_url_resolves(self):
        """Test the add review URL resolves correctly."""
        url = reverse("add_review", args=[1])
        self.assertEqual(resolve(url).func, views.add_review)

    def test_edit_review_url_resolves(self):
        """Test the edit review URL resolves correctly."""
        url = reverse("edit_review", args=[1, 1])
        self.assertEqual(resolve(url).func, views.edit_review)

    def test_delete_review_url_resolves(self):
        """Test the delete review URL resolves correctly."""
        url = reverse("delete_review", args=[1, 1])
        self.assertEqual(resolve(url).func, views.delete_review)

    def test_add_product_url_resolves(self):
        """Test the add product URL resolves correctly."""
        url = reverse("add_product")
        self.assertEqual(resolve(url).func, views.add_product)

    def test_edit_product_url_resolves(self):
        """Test the edit product URL resolves correctly."""
        url = reverse("edit_product", args=[1])
        self.assertEqual(resolve(url).func, views.edit_product)

    def test_delete_product_url_resolves(self):
        """Test the delete product URL resolves correctly."""
        url = reverse("delete_product", args=[1])
        self.assertEqual(resolve(url).func, views.delete_product)
