from django.apps import AppConfig


class ProductsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "products"

    def ready(self):
        """Import signals to activate custom model events."""
        import products.signals  # Ensure signals are imported
