from django.test import TestCase
from django.contrib.auth.models import User
from decimal import Decimal
from checkout.models import Order, OrderLineItem
from products.models import Product
from profiles.models import UserProfile


class OrderModelTests(TestCase):
    def setUp(self):
        # Create a test user (signal creates UserProfile automatically)
        self.user = User.objects.create_user(
            username="testuser", password="password"
        )

        # Fetch the automatically created UserProfile
        self.user_profile = UserProfile.objects.get(user=self.user)

        # Create a product
        self.product = Product.objects.create(
            name="Test Product",
            price=Decimal("10.00"),
            stock_quantity=10,
            sku="TESTSKU",
        )

        # Create an order
        self.order = Order.objects.create(
            user_profile=self.user_profile,
            full_name="John Doe",
            email="johndoe@example.com",
            phone_number="123456789",
            country="US",
            town_or_city="Test City",
            street_address1="123 Test St",
            delivery_cost=Decimal("5.00"),
            order_total=Decimal("0.00"),
            grand_total=Decimal("0.00"),
            original_bag="{}",
            stripe_pid="testpid123",
        )

    def test_generate_order_number(self):
        """Test that the order number is generated correctly."""
        order_number = self.order._generate_order_number()
        self.assertTrue(order_number, "Order number should not be empty.")
        self.assertTrue(
            order_number.isupper(), "Order number should be uppercase."
        )

    def test_save_method(self):
        """Test that the save method generates an order number."""
        order = Order.objects.create(
            user_profile=self.user_profile,
            full_name="Jane Doe",
            email="janedoe@example.com",
            phone_number="987654321",
            country="US",
            town_or_city="Another City",
            street_address1="456 Another St",
        )
        self.assertTrue(
            order.order_number, "Order number should be generated upon save."
        )

    def test_update_total(self):
        """Test that the total and grand total are updated correctly."""
        OrderLineItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=3,
            lineitem_total=self.product.price * 3,
        )
        self.order.update_total()
        self.assertEqual(self.order.order_total, Decimal("30.00"))
        self.assertEqual(
            self.order.delivery_cost, Decimal("3.00")
        )  # Assuming delivery cost logic
        self.assertEqual(self.order.grand_total, Decimal("33.00"))

    def test_order_str(self):
        """Test the string representation of the order."""
        self.assertEqual(str(self.order), self.order.order_number)


class OrderLineItemModelTests(TestCase):
    def setUp(self):
        # Create a test user (signal creates UserProfile automatically)
        self.user = User.objects.create_user(
            username="testuser", password="password"
        )

        # Fetch the automatically created UserProfile
        self.user_profile = UserProfile.objects.get(user=self.user)

        # Create a product
        self.product = Product.objects.create(
            name="Test Product",
            price=Decimal("10.00"),
            stock_quantity=10,
            sku="TESTSKU",
        )

        # Create an order
        self.order = Order.objects.create(
            user_profile=self.user_profile,
            full_name="John Doe",
            email="johndoe@example.com",
            phone_number="123456789",
            country="US",
            town_or_city="Test City",
            street_address1="123 Test St",
        )

    def test_save_method(self):
        """Test the save method calculates the line item total and deducts stock."""
        line_item = OrderLineItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=3,
        )
        self.assertEqual(line_item.lineitem_total, Decimal("30.00"))
        self.assertEqual(self.product.stock_quantity, 7)

    def test_line_item_str(self):
        """Test the string representation of the line item."""
        line_item = OrderLineItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=1,
        )
        expected_str = (
            f"SKU {self.product.sku} on order {self.order.order_number}"
        )
        self.assertEqual(str(line_item), expected_str)
