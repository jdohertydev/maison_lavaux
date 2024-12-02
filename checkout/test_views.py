from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch
from decimal import Decimal
from django.contrib.messages import get_messages
from .models import Order, OrderLineItem
from products.models import Product
from profiles.models import UserProfile


class CheckoutViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.product = Product.objects.create(
            name="Test Product",
            price=Decimal("10.00"),
            stock_quantity=10,
            sku="TESTSKU",
        )
        self.user = UserProfile.objects.create(user=None)  # Replace with real user creation if needed

    @patch("stripe.PaymentIntent.create")
    def test_checkout_get_authenticated(self, mock_payment_intent):
        """Test GET request to checkout page for authenticated user."""
        mock_payment_intent.return_value = {"client_secret": "test_secret"}
        session = self.client.session
        session["bag"] = {self.product.id: 1}
        session.save()

        response = self.client.get(reverse("checkout"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "checkout/checkout.html")
        self.assertIn("order_form", response.context)
        self.assertIn("stripe_public_key", response.context)
        self.assertEqual(response.context["client_secret"], "test_secret")

    def test_checkout_get_empty_bag(self):
        """Test GET request to checkout page with an empty bag."""
        response = self.client.get(reverse("checkout"))
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertRedirects(response, reverse("products"))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "There's nothing in your bag at the moment")

    @patch("stripe.PaymentIntent.create")
    def test_checkout_post_valid_data(self, mock_payment_intent):
        """Test POST request to checkout with valid data."""
        mock_payment_intent.return_value = {"client_secret": "test_secret"}
        session = self.client.session
        session["bag"] = {self.product.id: 2}
        session.save()

        form_data = {
            "full_name": "John Doe",
            "email": "johndoe@example.com",
            "phone_number": "123456789",
            "country": "US",
            "postcode": "12345",
            "town_or_city": "Test City",
            "street_address1": "123 Test St",
            "street_address2": "",
            "county": "Test County",
        }
        response = self.client.post(reverse("checkout"), form_data)
        self.assertRedirects(response, reverse("checkout_success", args=[Order.objects.first().order_number]))

    def test_checkout_post_invalid_data(self):
        """Test POST request to checkout with invalid data."""
        session = self.client.session
        session["bag"] = {self.product.id: 2}
        session.save()

        form_data = {
            "full_name": "",  # Invalid empty field
            "email": "invalid-email",
            "phone_number": "123456789",
            "country": "US",
            "postcode": "12345",
            "town_or_city": "Test City",
            "street_address1": "123 Test St",
            "street_address2": "",
            "county": "Test County",
        }
        response = self.client.post(reverse("checkout"), form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "checkout/checkout.html")
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "There was an error with your form. Please double-check your information.")

    @patch("stripe.PaymentIntent.modify")
    def test_cache_checkout_data(self, mock_payment_intent_modify):
        """Test the cache_checkout_data view."""
        session = self.client.session
        session["bag"] = {self.product.id: 2}
        session.save()

        form_data = {
            "client_secret": "test_secret",
            "save_info": True,
        }
        response = self.client.post(reverse("cache_checkout_data"), form_data)
        self.assertEqual(response.status_code, 200)

    def test_checkout_success(self):
        """Test the checkout_success view."""
        order = Order.objects.create(
            full_name="John Doe",
            email="johndoe@example.com",
            phone_number="123456789",
            country="US",
            town_or_city="Test City",
            street_address1="123 Test St",
            delivery_cost=Decimal("5.00"),
            order_total=Decimal("20.00"),
            grand_total=Decimal("25.00"),
            stripe_pid="testpid123",
        )

        response = self.client.get(reverse("checkout_success", args=[order.order_number]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "checkout/checkout_success.html")
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), f"Order successfully processed! Your order number is {order.order_number}.")
