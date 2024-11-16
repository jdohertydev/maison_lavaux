from django.db import models
from products.models import Product
from django.contrib.auth.models import User

class SalesData(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sales_data')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='sales')
    views = models.IntegerField(default=0)  # Track product views
    purchases = models.IntegerField(default=0)  # Track product purchases
    added_to_cart = models.IntegerField(default=0)  # Track how often a product is added to the cart
    revenue_generated = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Revenue for the product
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the record was created
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp for the last update

    def __str__(self):
        return f"Analytics for {self.product.name}"
