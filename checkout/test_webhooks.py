from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch, MagicMock
from django.conf import settings


class WebhookViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("webhook")

        self.payload = (
            b'{"id": "evt_test_webhook", "type": "payment_intent.succeeded"}'
        )
        self.sig_header = "test_signature"
        self.wh_secret = "whsec_test_secret"
        settings.STRIPE_WH_SECRET = self.wh_secret
        settings.STRIPE_SECRET_KEY = "sk_test_secret_key"

    @patch("stripe.Webhook.construct_event")
    @patch(
        "checkout.webhook_handler.StripeWH_Handler.handle_payment_intent_succeeded"
    )
    def test_valid_payment_intent_succeeded(
        self, mock_handler, mock_construct_event
    ):
        """Test handling a valid payment_intent.succeeded webhook event."""
        mock_construct_event.return_value = {
            "id": "evt_test_webhook",
            "type": "payment_intent.succeeded",
        }
        mock_handler.return_value = MagicMock(status_code=200)

        response = self.client.post(
            self.url,
            data=self.payload,
            content_type="application/json",
            HTTP_STRIPE_SIGNATURE=self.sig_header,
        )

        # Assertions
        self.assertEqual(response.status_code, 200)
        mock_construct_event.assert_called_once_with(
            self.payload, self.sig_header, self.wh_secret
        )
        mock_handler.assert_called_once()

    @patch("stripe.Webhook.construct_event")
    @patch("checkout.webhook_handler.StripeWH_Handler.handle_event")
    def test_generic_event_handler(self, mock_handler, mock_construct_event):
        """Test handling a generic/unknown event."""
        mock_construct_event.return_value = {
            "id": "evt_test_webhook",
            "type": "unknown_event",
        }
        mock_handler.return_value = MagicMock(status_code=200)

        response = self.client.post(
            self.url,
            data=self.payload,
            content_type="application/json",
            HTTP_STRIPE_SIGNATURE=self.sig_header,
        )

        # Assertions
        self.assertEqual(response.status_code, 200)
        mock_construct_event.assert_called_once_with(
            self.payload, self.sig_header, self.wh_secret
        )
        mock_handler.assert_called_once()

    @patch(
        "stripe.Webhook.construct_event",
        side_effect=ValueError("Invalid payload"),
    )
    def test_invalid_payload(self, mock_construct_event):
        """Test handling an invalid payload."""
        response = self.client.post(
            self.url,
            data=self.payload,
            content_type="application/json",
            HTTP_STRIPE_SIGNATURE=self.sig_header,
        )

        # Assertions
        self.assertEqual(response.status_code, 400)
        mock_construct_event.assert_called_once_with(
            self.payload, self.sig_header, self.wh_secret
        )

    @patch(
        "stripe.Webhook.construct_event",
        side_effect=stripe.error.SignatureVerificationError(
            "Invalid signature", None
        ),
    )
    def test_invalid_signature(self, mock_construct_event):
        """Test handling an invalid signature."""
        response = self.client.post(
            self.url,
            data=self.payload,
            content_type="application/json",
            HTTP_STRIPE_SIGNATURE=self.sig_header,
        )

        # Assertions
        self.assertEqual(response.status_code, 400)
        mock_construct_event.assert_called_once_with(
            self.payload, self.sig_header, self.wh_secret
        )

    @patch(
        "stripe.Webhook.construct_event",
        side_effect=Exception("Unexpected error"),
    )
    def test_unexpected_exception(self, mock_construct_event):
        """Test handling an unexpected exception."""
        response = self.client.post(
            self.url,
            data=self.payload,
            content_type="application/json",
            HTTP_STRIPE_SIGNATURE=self.sig_header,
        )

        # Assertions
        self.assertEqual(response.status_code, 400)
        self.assertIn("Unexpected error", response.content.decode())
        mock_construct_event.assert_called_once_with(
            self.payload, self.sig_header, self.wh_secret
        )
