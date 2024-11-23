from django.test import TestCase
from products.models import Product
from analytics.models import SalesData
from django.contrib.auth.models import User


class SalesDataModelTest(TestCase):
    def setUp(self):
        """Set up test data for SalesData model."""
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.product = Product.objects.create(
            name='Luxury Perfume',
            price=100.00,
            description='A premium fragrance.',
            stock_quantity=10
        )
        self.sales_data = SalesData.objects.create(
            product=self.product,
            user=self.user,
            views=25,
            purchases=10,
            added_to_cart=15,
            revenue_generated=1000.00
        )

    def test_sales_data_creation(self):
        """Test that the SalesData record is created correctly."""
        self.assertEqual(self.sales_data.product, self.product)
        self.assertEqual(self.sales_data.user, self.user)
        self.assertEqual(self.sales_data.views, 25)
        self.assertEqual(self.sales_data.purchases, 10)
        self.assertEqual(self.sales_data.added_to_cart, 15)
        self.assertEqual(self.sales_data.revenue_generated, 1000.00)

    def test_default_values(self):
        """Test that default values are set correctly."""
        sales_data_default = SalesData.objects.create(product=self.product)
        self.assertEqual(sales_data_default.views, 0)
        self.assertEqual(sales_data_default.purchases, 0)
        self.assertEqual(sales_data_default.added_to_cart, 0)
        self.assertEqual(sales_data_default.revenue_generated, 0)

    def test_updated_at_changes_on_save(self):
        """Test that the updated_at field changes when the record is saved."""
        initial_updated_at = self.sales_data.updated_at
        self.sales_data.views += 1
        self.sales_data.save()
        self.assertNotEqual(self.sales_data.updated_at, initial_updated_at)

    def test_sales_data_str_method(self):
        """Test the string representation of the SalesData model."""
        self.assertEqual(str(self.sales_data), f"Analytics for {self.product.name}")
