from django.apps import AppConfig


class CheckoutConfig(AppConfig):
    """Configuration for the checkout app."""

    name = "checkout"

    def ready(self):
        """Import signals when the app is ready."""
        import checkout.signals
