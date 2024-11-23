from django.test import TestCase
from django.urls import reverse
from products.models import Product, Category


class ProductViewsTest(TestCase):
    def setUp(self):
        """Set up data for testing views."""
        # Create a category
        self.category = Category.objects.create(name="Fragrances")
        
        # Create products
        self.product1 = Product.objects.create(
            category=self.category,
            sku="SKU123",
            name="Luxury Perfume",
            description="A premium unisex fragrance.",
            price=100.00,
            stock_quantity=50
        )
        self.product2 = Product.objects.create(
            category=self.category,
            sku="SKU124",
            name="Budget Perfume",
            description="An affordable fragrance.",
            price=20.00,
            stock_quantity=100
        )

    def test_product_list_view(self):
        """Test the product list view renders correctly."""
        response = self.client.get(reverse('products'))  # Ensure the URL name is correct
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/products.html')  # Adjust template if needed
        self.assertContains(response, self.product1.name)
        self.assertContains(response, self.product2.name)

    def test_product_detail_view(self):
        """Test the product detail view."""
        response = self.client.get(reverse('product_detail', args=[self.product1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product_detail.html')  # Adjust template if needed
        self.assertContains(response, self.product1.name)
        self.assertContains(response, self.product1.description)

    def test_category_filter_view(self):
        """Test the product list view with category filtering."""
        response = self.client.get(reverse('products'), {'category': self.category.name})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product1.name)
        self.assertContains(response, self.product2.name)

    def test_out_of_stock_product(self):
        self.product1.stock_quantity = 0
        self.product1.save()
        response = self.client.get(reverse('products'))
        self.assertContains(response, self.product1.name)  # Out-of-stock products are displayed

