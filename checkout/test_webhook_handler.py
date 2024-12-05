from django.test import TestCase
from django.http import HttpRequest
from unittest.mock import patch, MagicMock
from decimal import Decimal
from .models import Order, OrderLineItem
from products.models import Product
from profiles.models import UserProfile
from .webhook_handler import StripeWH_Handler


class StripeWH_HandlerTests(TestCase):
    def setUp(self):
        # Set up a mock request and handler
        self.request = HttpRequest()
        self.handler = StripeWH_Handler(self.request)

        # Set up a product
        self.product = Product.objects.create(
            name="Test Product",
            price=Decimal("10.00"),
            stock_quantity=10,
            sku="TESTSKU",
        )

        # Mock event data
        self.event_data = {
            "type": "payment_intent.succeeded",
            "data": {
                "object": {
                    "id": "pi_12345",
                    "metadata": {
                        "bag": '{"1": 2}',
                        "save_info": True,
                        "username": "testuser",
                    },
                    "shipping": {
                        "name": "John Doe",
                        "phone": "123456789",
                        "address": {
                            "line1": "123 Test St",
                            "line2": "",
                            "city": "Test City",
                            "state": "Test State",
                            "postal_code": "12345",
                            "country": "US",
                        },
                    },
                },
            },
        }

    @patch("checkout.webhook_handler.send_mail")
    @patch("stripe.Charge.retrieve")
    def test_handle_payment_intent_succeeded(
        self, mock_charge_retrieve, mock_send_mail
    ):
        """Test handling payment_intent.succeeded event."""
        mock_charge_retrieve.return_value = MagicMock(
            amount=2000,
            billing_details=MagicMock(email="testuser@example.com"),
        )

        response = self.handler.handle_payment_intent_succeeded(
            self.event_data
        )

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertIn("SUCCESS", response.content.decode())

        # Check if order was created
        order = Order.objects.get(stripe_pid="pi_12345")
        self.assertEqual(order.full_name, "John Doe")
        self.assertEqual(order.grand_total, Decimal("20.00"))

        # Check if order line items were created
        line_item = OrderLineItem.objects.get(
            order=order, product=self.product
        )
        self.assertEqual(line_item.quantity, 2)

        # Check if confirmation email was sent
        mock_send_mail.assert_called_once()

    def test_handle_event(self):
        """Test handling an unknown event."""
        event = {"type": "unknown.event"}
        response = self.handler.handle_event(event)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Unhandled webhook received", response.content.decode())

    @patch("checkout.webhook_handler.logging.error")
    def test_handle_payment_intent_succeeded_error(self, mock_logging_error):
        """Test error handling during order creation."""
        self.event_data["data"]["object"]["metadata"][
            "bag"
        ] = '{"999": 2}'  # Invalid product ID
        response = self.handler.handle_payment_intent_succeeded(
            self.event_data
        )

        # Assertions
        self.assertEqual(response.status_code, 500)
        self.assertIn("ERROR", response.content.decode())
        mock_logging_error.assert_called_once()

    def test_handle_payment_intent_payment_failed(self):
        """Test handling payment_intent.payment_failed event."""
        event = {"type": "payment_intent.payment_failed"}
        response = self.handler.handle_payment_intent_payment_failed(event)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Webhook received", response.content.decode())
