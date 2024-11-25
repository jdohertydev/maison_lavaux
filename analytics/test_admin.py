from django.test import TestCase, RequestFactory
from analytics.admin import RevenueFilter
from analytics.models import SalesData
from products.models import Product


class TestRevenueFilter(TestCase):
    """
    Unit tests for the RevenueFilter class in the admin interface.
    Validates the filtering of sales data by revenue range.
    """

    def setUp(self):
        """Set up test data for RevenueFilter."""
        self.product = Product.objects.create(
            name='Luxury Perfume',
            price=100.00,
            description='A premium fragrance.',
            stock_quantity=10,
        )
        SalesData.objects.create(product=self.product, revenue_generated=300.00)
        SalesData.objects.create(product=self.product, revenue_generated=1000.00)
        SalesData.objects.create(product=self.product, revenue_generated=3000.00)

    def test_revenue_filter_low(self):
        """Test the 'low' revenue range filter (< $500)."""
        class MockFilter(RevenueFilter):
            def value(self):
                return 'low'

        mock_filter = MockFilter(None, {}, None, None)
        queryset = mock_filter.queryset(None, SalesData.objects.all())
        self.assertEqual(queryset.count(), 1)
        self.assertEqual(queryset.first().revenue_generated, 300.00)

    def test_revenue_filter_medium(self):
        """Test the 'medium' revenue range filter ($500-$2000)."""
        class MockFilter(RevenueFilter):
            def value(self):
                return 'medium'

        mock_filter = MockFilter(None, {}, None, None)
        queryset = mock_filter.queryset(None, SalesData.objects.all())
        self.assertEqual(queryset.count(), 1)
        self.assertEqual(queryset.first().revenue_generated, 1000.00)

    def test_revenue_filter_high(self):
        """Test the 'high' revenue range filter (> $2000)."""
        class MockFilter(RevenueFilter):
            def value(self):
                return 'high'

        mock_filter = MockFilter(None, {}, None, None)
        queryset = mock_filter.queryset(None, SalesData.objects.all())
        self.assertEqual(queryset.count(), 1)
        self.assertEqual(queryset.first().revenue_generated, 3000.00)
