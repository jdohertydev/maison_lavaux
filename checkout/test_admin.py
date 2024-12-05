from django.test import TestCase
from django.contrib.admin.sites import AdminSite
from decimal import Decimal
from unittest.mock import Mock
from checkout.models import Order, OrderLineItem
from checkout.admin import OrderAdmin, OrderLineItemAdminInline
from products.models import Product


class MockRequest:
    """Mock request object for admin tests."""

    pass


class OrderAdminTests(TestCase):
    def setUp(self):
        # Create a test order
        self.order = Order.objects.create(
            order_number="ORD123",
            full_name="John Doe",
            email="johndoe@example.com",
            phone_number="123456789",
            country="US",
            postcode="12345",
            town_or_city="Test City",
            street_address1="123 Test St",
            street_address2="Apt 4B",
            county="Test County",
            delivery_cost=Decimal("5.00"),
            order_total=Decimal("50.00"),
            grand_total=Decimal("55.00"),
            original_bag="{}",
            stripe_pid="testpid123",
        )
        self.order_admin = OrderAdmin(Order, AdminSite())

    def test_total_items_method(self):
        """Test the total_items method for OrderAdmin."""
        # Add a product for the line item
        product = Product.objects.create(
            name="Test Product",
            price=Decimal("10.00"),
            stock_quantity=10,
            sku="TESTSKU",
        )

        # Add a line item to the order
        OrderLineItem.objects.create(
            order=self.order,
            product=product,
            quantity=3,
            lineitem_total=product.price * 3,
        )

        # Call the total_items method and verify its output
        result = self.order_admin.total_items(self.order)
        self.assertEqual(
            result,
            3,
            "total_items method does not return the correct total quantity.",
        )

    def test_formatted_grand_total_method(self):
        """Test the formatted_grand_total method for OrderAdmin."""
        result = self.order_admin.formatted_grand_total(self.order)
        self.assertEqual(
            result,
            "$55.00",
            "formatted_grand_total does not format the grand total correctly.",
        )


class OrderLineItemAdminInlineTests(TestCase):
    def setUp(self):
        # Create an instance of OrderLineItemAdminInline for testing
        self.inline = OrderLineItemAdminInline(OrderLineItem, AdminSite())

    def test_readonly_fields(self):
        """Ensure readonly fields for inline admin are properly set."""
        expected_readonly_fields = (
            "product",
            "product_size",
            "quantity",
            "lineitem_total",
        )
        self.assertEqual(
            self.inline.readonly_fields,
            expected_readonly_fields,
            "Readonly fields in OrderLineItemAdminInline do not match the expected list.",
        )
