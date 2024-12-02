from django.test import TestCase
from decimal import Decimal
from checkout.models import Order, OrderLineItem
from products.models import Product
from django.conf import settings


class OrderLineItemSignalsTests(TestCase):
    def setUp(self):
        # Create a product
        self.product = Product.objects.create(
            name="Test Product",
            price=Decimal("10.00"),
            stock_quantity=10,
            sku="TESTSKU",
        )

        # Create an order
        self.order = Order.objects.create(
            full_name="John Doe",
            email="johndoe@example.com",
            phone_number="123456789",
            country="US",
            town_or_city="Test City",
            street_address1="123 Test St",
            delivery_cost=Decimal("2.00"),
            order_total=Decimal("0.00"),
            grand_total=Decimal("0.00"),
            original_bag="{}",
            stripe_pid="testpid123",
        )

    def test_update_on_save_signal(self):
        """Test that the order total is updated when a line item is created or updated."""
        # Add a line item to the order
        line_item = OrderLineItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2,
            lineitem_total=self.product.price * 2,
        )
        self.order.refresh_from_db()
        expected_grand_total = Decimal("22.00")  # 2 items * 10.00 + 2.00 delivery cost
        self.assertEqual(
            self.order.grand_total,
            expected_grand_total,
            f"Expected grand_total to be {expected_grand_total} but got {self.order.grand_total}.",
        )

    def test_update_on_delete_signal(self):
        """Test that the order total is updated when a line item is deleted."""
        # Add a line item to the order
        line_item = OrderLineItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2,
            lineitem_total=self.product.price * 2,
        )
        self.order.refresh_from_db()
        line_item.delete()
        self.order.refresh_from_db()
        expected_grand_total = Decimal("2.00")  # Only delivery cost remains
        self.assertEqual(
            self.order.grand_total,
            expected_grand_total,
            f"Expected grand_total to be {expected_grand_total} after deletion but got {self.order.grand_total}.",
        )
